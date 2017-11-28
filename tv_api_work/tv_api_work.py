#!/usr/bin/env python3
"""tv_api_work.py , Module called by TV_viewer contains a class(TvApi) to handle the tv maze API """
# ========================= MODULE HEADER=======================================
# title             :tv_api_work.py
# description       :module called by TV_viewer contains a class to handle the API
# author            :Gavin Lyons
# date              :24/11/2017
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# mail              :glyons66@hotmail.com
# python_version    :3.6.0
# Api               :http://www.tvmaze.com/api


# ==========================IMPORTS======================
# Import the system modules needed to run
from datetime import datetime
import pytvmaze
from prettytable import PrettyTable

# ==================== ClASS SECTION===============================


class TvApi(object):
    """ Class to handle interaction with tv maze API called by python program tv_viewer"""

    def __init__(self, name):
        self.tvshowtable = ""
        self.tvshow2table = ""
        self.tvshow3table = ""
        self.name = name
        self.tvn = pytvmaze.TVMaze()

    def extract_tv(self, row_no):
        """extracts tv show name from tv series table from given showname,
        called from method tv_showseries, returns datatable"""
        tv_show_name = ""
        try:
            row_no = int(row_no)
            # get name of show from row number
            tv_show_name = self.tvshowtable.get_string(border=False, header=False,
                                                       start=row_no, end=(row_no + 1),
                                                       fields=["seriesname"])
            # put tv data in table
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
            # TODO self.tvshow2table.add_row(["Favourite", "n/a"])
        except Exception as extract_tve:
            print("Except: in tv_api_work extract_tv, {}, {}".format(extract_tve, tv_show_name))
        return self.tvshow2table

    def search_tv_series(self, itemshow):
        """Search a Tv show, program status S1, takes in input text,
        Return table of finds or None"""
        try:
            items = pytvmaze.show_search(itemshow)
            self.tvshowtable = PrettyTable(vertical_char=" ")
            for i, item in enumerate(items):
                self.tvshowtable.field_names = [i+1, "seriesname"]
                self.tvshowtable.add_row([i, item])
        except Exception as search_tv_seriese:
            print("Except:tv-Api_work,searchtvseries,{},{}".format(search_tv_seriese, itemshow))
            self.tvshowtable = None
        return self.tvshowtable

    def show_tv_series(self, rowno):
        """Select a Tv show, program status S2, passed rowno user selected ,
        returns datatable or None"""
        try:
            # extract name
            item = self.extract_tv(rowno)
        except Exception as show_tv_seriese:
            print("Except: tv-Api_work, show_tv_series, {}, {}".format(show_tv_seriese, rowno))
            item = None
        return item

    def showname_get(self, mazeid):
        """method to calculate if valid maze_ID in API called from fav_edit ,
        takes in a maze ID returns a string with showname or error"""
        try:
            showname = self.tvn.get_show(maze_id=mazeid)
        except Exception as showname_gete:
            print("Except: tv-Api_work, showname_get, {} ,{}".format(showname_gete, mazeid))
            showname = "Error"
        return showname

    def favour_show(self, database):
        """mtd to display favs takes in list of tuple pairs
        from db returns the new data_table for display"""
        data_table = ""
        try:

            data_table = PrettyTable(vertical_char=" ", padding_width=6)
            for num, name in database:
                delta_date, next_release_date = self.tv_maze_date(name)
                data_table.field_names = ["Days till", "Next episode", "Maze_id", "series name" ]
                data_table.add_row([delta_date, next_release_date, num, name, ])
            data_table.isprintable(True)
        except Exception as favour_showe:
            print("Except: tv-Api_work, favour_show, {}".format(favour_showe))
        return data_table

    def tv_maze_date(self, showname):
        """ method to calculate days to next episode takes in showname
        returns deltadate and releaseDate"""
        try:
            show = self.tvn.get_show(show_name=showname)
            current_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            next_release_date = datetime.strptime(show.next_episode.airdate, '%Y-%m-%d').date()
            delta_date = (next_release_date - current_date.date()).days
        except Exception as tv_maze_datee:
            print("Except: tv_api_work, tv_maze_date, {}, {}".format(tv_maze_datee, showname))
            next_release_date = "n/a"
            delta_date = "n/a"
        return delta_date, next_release_date

    def overview(self, row_no):
        """ method to get overview of show passed in rowno returns the summary """
        try:
            row_no = int(row_no)
            # get name of show from row number passed
            tvshowname = self.tvshow2table.get_string(border=False, header=False,
                                                      start=row_no, end=(row_no + 1),
                                                      fields=["Value"])
            show = self.tvn.get_show(show_name=tvshowname)
            summary = str(show.summary)
        except Exception as overviewe:
            print("Except: tv_api_work, overview ,{} ,{}".format(overviewe, row_no))
            summary = overviewe
        return summary

    def seasons(self, row_no):
        """ method to get seasons of show passed in rowno returns the seasons"""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(border=False, header=False, start=row_no,
                                                  end=(row_no + 1),
                                                  fields=["Value"])

            seasons = pytvmaze.show_seasons(int(mazeid))
            self.tvshow3table = PrettyTable(vertical_char=" ")
            for i, item in enumerate(seasons):
                self.tvshow3table.field_names = [i+1, "season"]
                self.tvshow3table.add_row([i, item])
        except Exception as seasonse:
            print("Except: tv_api_work, seasons, {} , {}".format(seasonse, row_no))
        return self.tvshow3table

    def episode(self, row_no):
        """ method to get episode list of show passed
        in row no of table , returns the episodes """
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            maze_id = self.tvshow2table.get_string(border=False, header=False, start=row_no,
                                                   end=(row_no + 1), fields=["Value"])

            episode = pytvmaze.episode_list(int(maze_id), specials=None)
            self.tvshow3table = PrettyTable(vertical_char=" ")
            for i, item in enumerate(episode):
                self.tvshow3table.field_names = [i+1, "episode"]
                self.tvshow3table.add_row([i, item])
        except Exception as episodee:
            print("Except: tv_api_work, episode, {}, {}".format(episodee, row_no))
        return self.tvshow3table

    def actors(self, row_no):
        """ method to get actors info of show passed in row no of table ,
        returns the info """
        actor_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(border=False, header=False, start=row_no,
                                                  end=(row_no + 1), fields=["Value"])

            mycast = pytvmaze.show_cast(int(mazeid)).people
            actor_table = PrettyTable(vertical_char=" ")
            for i, people in enumerate(mycast):
                actor_table.field_names = [i, "Character", "Person"]
                actor_table.add_row([i, people.character.name, people.name])
        except Exception as actorse:
            print("Except: tv_api_work, actors, {} , {}".format(actorse, row_no))
        return actor_table

    def crews(self, row_no):
        """ method to get crews info of show passed in rowno returns the info """
        crew_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(border=False, header=False, start=row_no,
                                                  end=(row_no + 1), fields=["Value"])

            mycrew = pytvmaze.get_show_crew(int(mazeid))
            crew_table = PrettyTable(vertical_char=" ")
            for i, people in enumerate(mycrew):
                crew_table.field_names = [i, "Person", "Role"]
                crew_table.add_row([i, people.person.name, people.type])
        except Exception as crewse:
            print("Except: tv_api_work crews {} {}".format(crewse, row_no))
        return crew_table

    def more_info(self, row_no):
        """extracts tv show name from tv series table for a  given row number
        called from tvshowseries returns a datatable with show details"""
        data_table = ""
        tv_show_name = ""
        try:
            row_no = int(row_no)
            # get name of show from row number
            tv_show_name = self.tvshow2table.get_string(border=False, header=False,
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
        except Exception as more_infoe:
            print("Error: more_info, tv_api_work, {}, {}".format(more_infoe, tv_show_name))
        return data_table


# =====================MAIN===============================


def test(text):
    """ test import function"""
    print(text)


if __name__ == '__main__':
    test("main")
else:
    test("Imported {}".format(__name__))
# =====================END===============================
