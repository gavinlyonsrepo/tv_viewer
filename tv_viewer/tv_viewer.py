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
# version           :1.1
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
from tv_qt_class import tv_qt_class as myqt
from logger_conf import logger_conf as myLog

# =====================MAIN===============================
if __name__ == "__main__":
    logger = myLog.my_logging(__name__)
    logger.info("  Main Loop Start")
    app = QtWidgets.QApplication(sys.argv)
    if sys.platform == 'win32':
    	pass
    else:
    	app.setWindowIcon(QIcon('/usr/share/pixmaps/tv_viewer.png'))
    MainWindow = QtWidgets.QMainWindow()
    ui = myqt.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# =====================END===============================

