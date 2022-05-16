#!/usr/bin/env python3
""" tv_viewer : GUI to view tv program details using TV maze application
programming interface. Written in python 3 and PyQt 5,
it also stores user favourites in an
SQLite database. It uses python module pytvmaze to interface with API
and python module prettytable to help display results."""
# =========================MAIN SCRIPT HEADER==================
# title             :tv_viewer
# description       :Main Script
# author            :Gavin Lyons
# version           :2.0
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# python_version    :3.10.4

# ==========================IMPORTS======================
# Import the system modules needed to run
import sys
import os
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon


# My modules
from tv_qt_class import tv_qt_class as myqt
from tv_logger_conf import tv_logger_conf as my_log

# =====================MAIN===============================
if __name__ == "__main__":
    logger = my_log.my_logging(__name__)
    logger.info("  Main Loop Start")
    app = QtWidgets.QApplication(sys.argv)
    if sys.platform == 'win32':
        pass  # Icon not installed in windows version currently, TODO
    else:
        app.setWindowIcon(QIcon(os.environ['HOME'] + "/.local/share/icons/tv_viewer.png"))
    MainWindow = QtWidgets.QMainWindow()
    ui = myqt.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# =====================END===============================
