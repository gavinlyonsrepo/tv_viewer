#!/usr/bin/env python3
""" tv_viewer : GUI to view tv program details using TV maze application
programming interface. Written in python 3 and PyQt 5, it also stores user favourites in an
SQLite database. It uses python module pytvmaze to interface with API
and python module prettytable to help display results."""
# =========================MAIN SCRIPT HEADER=======================================
# title             :tv_viewer
# description       :Python PyQt5 GUI to view tv program details using tvmaze API and SQllite3 database
# author            :Gavin Lyons
# date              :20/08/2017
# version           :1.0
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# mail              :glyons66@hotmail.com
# python_version    :3.6.0
# main api:         :http://www.tvmaze.com/api

# ==========================IMPORTS======================
# Import the system modules needed to run

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

# My modules
from tv_qt_class import Ui_MainWindow as Myqt


# =====================MAIN===============================
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('/usr/share/pixmaps/tv_viewer.png'))
    Myqt.MainWindow = QtWidgets.QMainWindow()
    ui = Myqt()
    ui.setupUi(Myqt.MainWindow)
    Myqt.MainWindow.show()
    sys.exit(app.exec_())
# =====================END===============================
