#!/usr/bin/env python3
"""python script """
#=========================HEADER=======================================
# title             :
# description       :
# author            :Gavin Lyons
# date              :17/08/2017
# version           :
# web               :https://github.com/gavinlyonsrepo/
# mail              :glyons66@hotmail.com
# python_version    :

#==========================IMPORTS======================
# Import the system modules needed to run rpi_tempmon.py.
import pytvmaze
from datetime import datetime
from prettytable import PrettyTable

#my modules



#=======================GLOBALS=========================


#====================FUNCTION SECTION===============================



def searchTvSeries(itemShow):
    items = ""
    items = pytvmaze.show_search(itemShow)
    ptable = PrettyTable()
    for i, item in enumerate(items):
        ptable.field_names = [i, "seriesname"]
        ptable.add_row([i, item.name])
    print(ptable)
    return ptable



#=====================MAIN===============================

def test(text):
    """ docstring """
    print(text)


if __name__ == '__main__':
    test("main")
else:
    test("Imported tv_api_work")
#=====================END===============================
