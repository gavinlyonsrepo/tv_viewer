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

# my modules



# =======================GLOBALS=========================


# ====================FUNCTION SECTION===============================


class Tvapi(object):

    def __init__(self, name):
            self.tvshowtable = ""
            self.name = name


    def tvMazeCreator(self, items, mainChoice, tvName=None):
            if tvName is not None:
                return pytvmaze.show_search(str(tvName))
            else:
                return pytvmaze.show_search(items[int(mainChoice)].name)[int(mainChoice)]

    def tvMazeDate(self, tvMaze):
            currentDate = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            try:
                nextReleaseDate = datetime.strptime(tvMaze.next_episode.airdate, '%Y-%m-%d').date()
                deltaDate = (nextReleaseDate - currentDate.date()).days
            except:
                nextReleaseDate = "---"
                deltaDate = "---"
            return deltaDate, nextReleaseDate

    def extractTV(self, rowno):
            print("extract function")
            print(rowno)
            print(self.tvshowtable)
            rowno = int(rowno)
            tvshowname = self.tvshowtable.get_string(start=rowno, end=(rowno + 1), fields=["seriesname"])
            print(tvshowname)
            return tvshowname


    def searchTvSeries(self, itemShow):
            """Search a Tv show program status S1, Return table of finds"""
            try:
                items = ""
                items = pytvmaze.show_search(itemShow)
                self.tvshowtable = PrettyTable()
                for i, item in enumerate(items):
                    self.tvshowtable.field_names = [i, "seriesname"]
                    self.tvshowtable.add_row([i, item])
            except Exception:
                print("There Is No Matching Tv Show")
                self.tvshowtable = False
            return self.tvshowtable

    def showTvSeries(self, tvshow):
            """Select a Tv show program status S1"""
            try:
                item = ""
                # extract name
                 print(tvshow)
                 item = self.extractTV(tvshow)
                 print(item)
                 #pytvmaze.get_show(item)
            except Exception as e:
                print(e)
                print("There Is No Matching Row number")

            return item


# =====================MAIN===============================

def test(text):
    """ docstring """
    print(text)


if __name__ == '__main__':
    test("main")
else:
    test("Imported tv_api_work")
#=====================END===============================
