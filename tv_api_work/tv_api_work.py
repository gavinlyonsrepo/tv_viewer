#!/usr/bin/env python3
"""
filename :tv_api_work.py
Description: Module called by TV_viewer
    contains a class(TvApi) to handle interaction with the tv maze API class 
    Also contains a class SimpleTable to turn API data into formatted table
    for display in GUI.
"""

# ==========================IMPORTS======================
# Import the system modules needed to run

from datetime import datetime
# my modules
from tv_logger_conf import tv_logger_conf as my_log
from tv_sqllite import tv_sqllite as mySql
# files from this module
from . import tv_maze as my_tvmaze
from .tv_maze_exceptions import BaseError


# ==========================GLOBALS===============================
# setup logging
logger = my_log.my_logging(__name__)

# ==================== ClASS SECTION===============================

# ==========================SIMPLETABLE===========================

class SimpleTable:
    """Class to format API data into a table, for 
    display in the GUI listbox information screen"""

    def __init__(self, **kwargs):
        self._field_names: list = []
        self._rows: list[list] = []
        self._padding_width: int = kwargs.get("padding_width", 1)
        self._align: str = kwargs.get("align", "l")
        self._col_align: dict = {}

    @property
    def field_names(self) -> list:
        """Return the list of column header names."""
        return self._field_names

    @field_names.setter
    def field_names(self, names: list):
        """Set the column header names, converting input to a list."""
        self._field_names = list(names)

    def add_row(self, row: list):
        """ Adds a row to the list"""
        self._rows.append(list(row))

    def _col_widths(self) -> list[int]:
        """Calculate max width for each column across header and all rows."""
        widths = [len(str(f)) for f in self._field_names]
        for row in self._rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        return widths

    def _make_border(self, widths: list[int]) -> str:
        """Build a +------+-------+ border line."""
        pad = self._padding_width
        parts = ["-" * (w + pad * 2) for w in widths]
        return "+" + "+".join(parts) + "+"

    def set_col_align(self, col_name: str, align: str):
        """Set alignment for a specific column: 'l', 'r', or 'c'."""
        self._col_align[col_name] = align

    def _make_row(self, row: list, widths: list[int]) -> str:
        pad = " " * self._padding_width
        cells = []
        for i, w in enumerate(widths):
            cell = str(row[i]).strip() if i < len(row) else ""  # strip each cell
            col_name = str(self._field_names[i]) if i < len(self._field_names) else ""
            align = self._col_align.get(col_name, self._align)
            if align == "r":
                cells.append(pad + cell.rjust(w) + pad)
            elif align == "c":
                cells.append(pad + cell.center(w) + pad)
            else:
                cells.append(pad + cell.ljust(w) + pad)
        return " " + " ".join(cells) + " "

    def get_string(
        self,
        header: bool = True,
        start: int = 0,
        end: int | None = None,
        fields: list | None = None,
         ) -> str:
        """Return a plain-text rendering of a row slice."""
        if fields is not None:
            try:
                col_indices = [self._field_names.index(f) for f in fields]
            except ValueError:
                col_indices = list(range(len(self._field_names)))
        else:
            col_indices = list(range(len(self._field_names)))
        row_slice = self._rows[start:end]
        lines = []
        pad = " " * self._padding_width
        if header and self._field_names:
            header_cells = [str(self._field_names[i]) for i in col_indices]
            lines.append(pad.join(header_cells))

        for row in row_slice:
            cells = [str(row[i]) for i in col_indices if i < len(row)]
            lines.append(pad.join(cells))
        return "\n".join(lines)

    def __str__(self) -> str:
        """Full table with +--+--+ borders."""
        if not self._field_names:
            return ""
        widths = self._col_widths()
        border = self._make_border(widths)
        lines = [
            border,
            self._make_row(self._field_names, widths),
            border,
        ]
        for row in self._rows:
            lines.append(self._make_row(row, widths))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()



class TvApi():
    """ Class to handle interaction with
    tv maze API class called by python program tv_viewer"""

    def __init__(self, name):
        self.tvshowtable = ""  # used to display list of shows
        self.tvshow2table = ""   # used to display show info
        self.name = name
        self.tvn = my_tvmaze.TVMaze()
        # define instance of the SQl class for favourate view
        self.my_tv_sql = mySql.TvSqLight("mysqlobject1")

    def search_tv_series(self, itemshow):
        """Search for a Tv show, program status S1,
        takes in input text from user,
        Return table of finds or None"""
        try:
            items = my_tvmaze.show_search(itemshow)
            self.tvshowtable = SimpleTable()
            for i, item in enumerate(items):
                self.tvshowtable.field_names = [i+1, "seriesname"]
                self.tvshowtable.add_row([i, item])
        except BaseError:
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
                    header=False,
                    start=row_no, end=(row_no + 1),
                    fields=["seriesname"])
            else:
                tv_show_name = show_name
            # put tv data in new table
            show = self.tvn.get_show(show_name=tv_show_name)
            delta_date, next_release_date = self.tv_maze_date(tv_show_name)
            self.tvshow2table = SimpleTable()
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
        except (BaseError, ValueError, AttributeError):
            logger.exception("Failure to extract info for TV show :: %s ", tv_show_name)
            self.tvshow2table = None
        return self.tvshow2table

    def showname_get(self, mazeid):
        """method to calculate if valid maze_ID in API called from fav_edit ,
        takes in a maze ID returns a string with showname or error"""
        try:
            showname = self.tvn.get_show(maze_id=mazeid)
        except (BaseError, ValueError, AttributeError):
            logger.exception(" Failure to find maze_ID %s ", mazeid)
            showname = "Error"
        return showname

    def favour_show(self, database):
        """mtd to display favs takes in list of tuple pairs
        from db returns the new data_table for display"""
        data_table = []
        try:
            if database:
                data_table = SimpleTable(padding_width=5, align="l")
                data_table.set_col_align("Maze_id", "r")
                for num, name in database:
                    delta_date, next_release_date = self.tv_maze_date(name)
                    num = str(num).rjust(5, '0')  # Pad the number with zeros
                    data_table.field_names = ["Next epi", "Days till", "Maze_id", "Series"]
                    data_table.add_row([next_release_date, delta_date, str(num), name])
        except (BaseError, ValueError, AttributeError):
            logger.exception(" Failure to show favs :: ")
        return data_table

    def tv_maze_date(self, showname):
        """ method to calculate days to next episode takes in showname
        returns days to next episode and release Date"""
        try:
            show = self.tvn.get_show(show_name=showname)
            current_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            next_release_date = datetime.strptime(show.next_episode.airdate, '%Y-%m-%d').date()
            delta_date = (next_release_date - current_date.date()).days
            if delta_date == -1:
                delta_date = "NoW"
            else:
                delta_date = str(delta_date).rjust(3, '0')  # Pad the number with zeros

        except (BaseError, ValueError, AttributeError, TypeError):
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
                header=False,
                start=row_no, end=(row_no + 1),
                fields=["Value"])
            show = self.tvn.get_show(show_name=tvshowname)
            summary = str(show.summary)
        except (BaseError, ValueError, AttributeError):
            logger.warning(" Failure to get summary :: %s", tvshowname)
        return summary

    def seasons(self, row_no):
        """ method to get seasons of show passed
        in row no returns the seasons data"""
        season_table = ""
        try:
            row_no = int(row_no)
            # get number of show from row number passed
            mazeid = self.tvshow2table.get_string(
                header=False, start=row_no,
                end=(row_no + 1),
                fields=["Value"])

            seasons = my_tvmaze.show_seasons(int(mazeid))
            season_table = SimpleTable()
            for i, item in enumerate(seasons):
                season_table.field_names = [i+1, "season"]
                season_table.add_row([i, item])
        except (BaseError, ValueError, AttributeError):
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
                header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            episode = my_tvmaze.episode_list(int(maze_id), specials=None)
            epi_table = SimpleTable(vertical_char=" ")
            for i, item in enumerate(episode):
                epi_table.field_names = [i+1, "episode"]
                epi_table.add_row([i, item])
        except (BaseError, ValueError, AttributeError):
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
                header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            mycast = my_tvmaze.show_cast(int(mazeid)).people
            actor_table = SimpleTable()
            for i, people in enumerate(mycast):
                actor_table.field_names = [i, "Character", "Person"]
                actor_table.add_row([i, people.character.name, people.name])
        except (BaseError, ValueError, AttributeError):
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
                header=False, start=row_no,
                end=(row_no + 1), fields=["Value"])

            mycrew = my_tvmaze.get_show_crew(int(mazeid))
            crew_table = SimpleTable()
            for i, people in enumerate(mycrew):
                crew_table.field_names = [i, "Person", "Role"]
                crew_table.add_row([i, people.person.name, people.type])
        except (BaseError, ValueError, AttributeError):
            logger.warning(" Failure to get crews data :: %s", mazeid)
        return crew_table

    def more_info(self, row_no):
        """extracts tv show name from tv series table for a  given row number
        called from tvshowseries returns a data table with show details"""
        data_table = ""
        tv_show_name = ""
        try:
            row_no = int(row_no)
            # get name of show from row number
            tv_show_name = self.tvshow2table.get_string(
                header=False,
                start=row_no, end=(row_no + 1),
                fields=["Value"])
            # put tv data in table
            show = self.tvn.get_show(show_name=tv_show_name)
            data_table = SimpleTable()
            data_table.field_names = ["Key", "Value"]
            data_table.add_row(["Network", show.network.name])
            data_table.add_row(["Country", show.network.country])
            data_table.add_row(["Schedule Time", show.schedule['time']])
            data_table.add_row(["Schedule Days", show.schedule['days']])
            data_table.add_row(["Runtime", show.runtime])
        except (BaseError, ValueError, AttributeError):
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
