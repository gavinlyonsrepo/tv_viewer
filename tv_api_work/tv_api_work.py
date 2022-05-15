#!/usr/bin/env python3
"""tv_api_work.py , Module called by TV_viewer
contains a class(TvApi) to handle the tv maze API """
# ========================= MODULE HEADER======================
# title             :tv_api_work.py
# description       :module from TV_viewer contains a class to handle the API
# author            :Gavin Lyons
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# python_version    :3.10.4
# Api               :http://www.tvmaze.com/api


# ==========================IMPORTS======================
# Import the system modules needed to run

from datetime import datetime
import pytvmaze
from prettytable import PrettyTable
# my modules
from tv_logger_conf import tv_logger_conf as my_log
from tv_sqllite import tv_sqllite as mySql

# ==========================GLOBALS===============================
# setup logging
logger = my_log.my_logging(__name__)

# ==================== ClASS SECTION===============================


class TvApi():
    """ Class to handle interaction with
    tv maze API called by python program tv_viewer"""

    def __init__(self, name):
        self.tvshowtable = ""  # used to display list of shows
        self.tvshow2table = ""   # used to display show info
        self.name = name
        self.tvn = pytvmaze.TVMaze()
        # define instance of the SQl class for favourate view
        self.my_tv_sql = mySql.TvSqLight("mysqlobject1")

    def search_tv_series(self, itemshow):
        """Search for a Tv show, program status S1,
        takes in input text from user,
        Return table of finds or None"""
        try:
            items = pytvmaze.show_search(itemshow)
            self.tvshowtable = PrettyTable(vertical_char=" ")
            for i, item in enumerate(items):
                self.tvshowtable.field_names = [i+1, "seriesname"]
                self.tvshowtable.add_row([i, item])
        except pytvmaze.BaseError:
            logger.exception(" Failure to find tv series :: %s ", itemshow)
            self.tvshowtable = None
        return self.tvshowtable

    def show_tv_series(self, row_no, show_name):
        """method to Select a Tv show, program status S2,
        passed row number user selected ,
        returns datatable of extracted info or None"""

        try:
            if show_name == "No show name":
                row_no = int(row_no)
                # get name of show from row number
                tv_show_name = self.tvshowtable.get_string(
                    border=False, header=False,
                    start=row_no, end=(row_no + 1),
                    fields=["seriesname"])
            else:
                tv_show_name = show_name

            # put tv data in new table
            show = self.tvn.get_show(show_name=tv_show_name)
            delta_date, next_release_date = self.tv_maze_date(tv_show_name)
            self.tvshow2table = PrettyTable(vertical_char=" ")
            self.tvshow2table.field_names = ["Key", "Value"]
            self.tvshow2table.add_row(["Maze_id", show.maze_id])
            self.tvshow2table.add_row(["Name", show.name])
            self.tvshow2table.add_row(["Rating", show.rating])
            self.tvshow2table.add_row(["Genre", show.genres])
            self.tvshow2table.add_row(["Status", show.status])
            self.tvshow2table.add_row(["Premiered ", show.premiered])
            self.tvshow2table.add_row(["Last episode", show.previous_episode.airdate])
            self.tvshow2table.add_row(["Next episode", next_release_date])
            self.tvshow2table.add_row(["Season / epi",
                                       str(show.previous_episode.season_number)
                                       + "/" + str(show.previous_episode.episode_number)])
            self.tvshow2table.add_row(["days to next", delta_date])
            # scan the database to see if its a fav
            show_flag = self.my_tv_sql.scan_db(show.maze_id)
            if show_flag:  # True its in favs database
                self.tvshow2table.add_row(["Favourite", "TRUE"])
            else:
                self.tvshow2table.add_row(["Favourite", "FALSE"])
        except Exception:
            logger.exception("Failure to extract info for TV show :: %s ", tv_show_name)
            self.tvshow2table = None
        return self.tvshow2table

    def showname_get(self, mazeid):
        """method to calculate if valid maze_ID in API called from fav_edit ,
        takes in a maze ID returns a string with showname or error"""
        try:
            showname = self.tvn.get_show(maze_id=mazeid)
        except Exception:
            logger.exception(" Failure to find maze_ID %s ", mazeid)
            showname = "Error"
        return showname

    def favour_show(self, database):
        """mtd to display favs takes in list of tuple pairs
        from db returns the new data_table for display"""
        data_table = []
        try:
            if database:
                data_table = PrettyTable(
                    vertical_char=" ", padding_width=5, align="l")
                for num, name in database:
                    delta_date, next_release_date = self.tv_maze_date(name)
                    data_table.field_names = ["Next epi", "Days till", "Maze_id", "Series"]
                    data_table.add_row([next_release_date, delta_date, str(num), name])
        except Exception:
            logger.exception(" Failure to show favs :: ")
        return data_table

    def tv_maze_date(self, showname):
        """ method to calculate days to next episode takes in showname
        returns days to next episode  and release Date"""
        try:
            show = self.tvn.get_show(show_name=showname)
            current_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            next_release_date = datetime.strptime(show.next_episode.airdate, '%Y-%m-%d').date()
            delta_date = (next_release_date - current_date.date()).days
            if delta_date == -1:
                delta_date = "NoW"
            else:
                delta_date = str(delta_date).rjust(3, '0')  # Pad the number with zeros

        except Exception:
            logger.info(" No next episode data : %s", showname)
            next_release_date = "0000-00-00"
            delta_date = "N/A"
        return delta_date, next_release_date

    def overview(self, row_no):
        """ method to get overview of show
        passed in row number  returns the summary """
        summary = ""
        try:
            row_no = int(row_no)
            # get name of show from row number passed
            tvshowname = self.tvshow2table.get_string(
                border=False, header=False,
                start=row_no, end=(row_no + 1),
                fields=["Value"])
            show = self.tvn.get_show(show_name=tvshowname)
            summary = str(show.summary)
        except Exception:
            logger.warning(" Failure to get summary :: %s", tvshowname)
        return summary

    def seasons(self, row_no):
        """ method to get seasons of show passed
        in rowno returns the seasons"""
        season_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(
                border=False, header=False, start=row_no,
                end=(row_no + 1),
                fields=["Value"])

            seasons = pytvmaze.show_seasons(int(mazeid))
            season_table = PrettyTable(vertical_char=" ")
            for i, item in enumerate(seasons):
                season_table.field_names = [i+1, "season"]
                season_table.add_row([i, item])
        except Exception:
            logger.warning(" Failure to get seasons :: %s", mazeid)
        return season_table

    def episode(self, row_no):
        """ method to get episode list of show passed
        in row no of table , returns the episodes in a table """
        epi_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            maze_id = self.tvshow2table.get_string(
                border=False, header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            episode = pytvmaze.episode_list(int(maze_id), specials=None)
            epi_table = PrettyTable(vertical_char=" ")
            for i, item in enumerate(episode):
                epi_table.field_names = [i+1, "episode"]
                epi_table.add_row([i, item])
        except Exception:
            logger.exception(" Failure to get episodes data :: %s", maze_id)
        return epi_table

    def actors(self, row_no):
        """ method to get actors info of show
        passed in row no of table ,
        returns the info """
        actor_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(
                border=False, header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            mycast = pytvmaze.show_cast(int(mazeid)).people
            actor_table = PrettyTable(vertical_char=" ")
            for i, people in enumerate(mycast):
                actor_table.field_names = [i, "Character", "Person"]
                actor_table.add_row([i, people.character.name, people.name])
        except Exception:
            logger.warning(" Failure to get actors :: %s", mazeid)
        return actor_table

    def crews(self, row_no):
        """ method to get crews info of show
        passed in rowno returns the info """
        crew_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(
                border=False, header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            mycrew = pytvmaze.get_show_crew(int(mazeid))
            crew_table = PrettyTable(vertical_char=" ")
            for i, people in enumerate(mycrew):
                crew_table.field_names = [i, "Person", "Role"]
                crew_table.add_row([i, people.person.name, people.type])
        except Exception:
            logger.warning(" Failure to get crews data :: %s", mazeid)
        return crew_table

    def more_info(self, row_no):
        """extracts tv show name from tv series table for a  given row number
        called from tvshowseries returns a datatable with show details"""
        data_table = ""
        tv_show_name = ""
        try:
            row_no = int(row_no)
            # get name of show from row number
            tv_show_name = self.tvshow2table.get_string(
                border=False, header=False,
                start=row_no, end=(row_no + 1),
                fields=["Value"])
            # put tv data in table
            show = self.tvn.get_show(show_name=tv_show_name)
            data_table = PrettyTable(vertical_char=" ")
            data_table.field_names = ["Key", "Value"]
            data_table.add_row(["Network", show.network.name])
            data_table.add_row(["Country", show.network.country])
            data_table.add_row(["Schedule Time", show.schedule['time']])
            data_table.add_row(["Schedule Days", show.schedule['days']])
            data_table.add_row(["Runtime", show.runtime])
        except Exception:
            logger.exception(" Failure to get more info data :: %s", tv_show_name)
        return data_table


# =====================MAIN===============================


def test(text):
    """ test import function"""
    logger.info(text)


if __name__ == '__main__':
    test("main")
else:
    test(" Imported " + __name__)
# =====================END===============================
