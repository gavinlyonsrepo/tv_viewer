#!/usr/bin/env python3
"""python script """
# =========================HEADER=======================================
# title             :
# description       :
# author            :Gavin Lyons
# date              :17/08/2017
# version           :
# web               :https://github.com/gavinlyonsrepo/
# mail              :glyons66@hotmail.com
# python_version    :

# ==========================IMPORTS======================
# Import the system modules needed to run
import pytvmaze
from datetime import datetime
from prettytable import PrettyTable

# ==================== FUNCTION SECTION===============================


class Tvapi(object):

    def __init__(self, name):
            self.tvshowtable = ""
            self.tvshow2table = ""
            self.name = name
            self.tvn = pytvmaze.TVMaze()

    def extractTV(self, rowno):
        """extracts tv show name from tv series table"""
        try:
            rowno = int(rowno)
            tvshowname = self.tvshowtable.get_string(border=False, header=False, start=rowno, end=(rowno + 1), fields=["seriesname"])

            # put tv data in table
            show = self.tvn.get_show(show_name=tvshowname)
            deltaDate, nextReleaseDate = self.tvMazeDate(tvshowname)
            self.tvshow2table = PrettyTable(vertical_char=" ")
            self.tvshow2table.field_names = ["Key", "Value"]
            self.tvshow2table.add_row(["Maze_id", show.maze_id])
            self.tvshow2table.add_row(["Name", show.name])
            self.tvshow2table.add_row(["Rating", show.rating])
            self.tvshow2table.add_row(["Genre", show.genres])
            self.tvshow2table.add_row(["Status", show.status])
            self.tvshow2table.add_row(["Premiered ", show.premiered])
            self.tvshow2table.add_row(["Last episode", show.previous_episode.airdate])
            self.tvshow2table.add_row(["Next episode", nextReleaseDate])
            self.tvshow2table.add_row(["Season / epi", str(show.previous_episode.season_number) + "/" + str(show.previous_episode.episode_number)])
            self.tvshow2table.add_row(["days to next", deltaDate])
          # TODO self.tvshow2table.add_row(["Favourite", "n/a"])
        except Exception as error5:
            print(error5)
            print("There Is Not enough information")
        return self.tvshow2table

    def searchTvSeries(self, itemShow):
            """Search a Tv show program status S1, Return table of finds"""
            try:
                items = pytvmaze.show_search(itemShow)
                self.tvshowtable = PrettyTable(vertical_char=" ")
                for i, item in enumerate(items):
                    self.tvshowtable.field_names = [i, "seriesname"]
                    self.tvshowtable.add_row([i, item])
            except Exception as error2:
                print(error2)
                print("There Is No Matching Tv Show")
                self.tvshowtable = False
            return self.tvshowtable

    def showTvSeries(self, tvshow):
            """Select a Tv show program status S2"""
            try:
                item = ""
                # extract name
                item = self.extractTV(tvshow)
            except Exception as error3:
                print(error3)
                item = error3
            return item

    def showname_get(self, mazeid):
        showname = self.tvn.get_show(maze_id=mazeid)
        return showname

    def favour_show(self, database):
        """function to display favourates"""
        try:
            datatable = PrettyTable(vertical_char=" ")
            for num, name in database:
                deltaDate, nextReleaseDate = self.tvMazeDate(name)
                datatable.field_names = ["Maze_id", "seriesname", "Next episode", "Days to next"]
                datatable.add_row([num, name, nextReleaseDate, "1"])
        except Exception as error6:
            print(error6)
        return datatable


    def tvMazeDate(self, showname):
        show = self.tvn.get_show(show_name=showname)
        currentDate = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        try:
            nextReleaseDate = datetime.strptime(show.next_episode.airdate, '%Y-%m-%d').date()
            deltaDate = (nextReleaseDate - currentDate.date()).days
        except:
            nextReleaseDate = "---"
            deltaDate = "---"
        return deltaDate, nextReleaseDate

# =====================MAIN===============================


def test(text):
    """ test import function"""
    print(text)


if __name__ == '__main__':
    test("main")
else:
    test("Imported {}".format(__name__))
# =====================END===============================

