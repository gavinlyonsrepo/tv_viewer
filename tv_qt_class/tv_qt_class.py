#!/usr/bin/env python3
"""tv_qt_class.py module called by tv_viewer contains a class to handle the PyQt5 GUI of program"""
# =========================MODULE HEADER=======================================
# title             :tv_qt_class
# description       :Module called by tv_viewer contains a class to handle the PyQt5 GUI of program
# author            :Gavin Lyons
# date              :20/11/2017
# web               :https://github.com/gavinlyonsrepo/
# mail              :glyons66@hotmail.com
# python_version    :3.6.0

# ==========================IMPORTS======================
# Import the system modules needed to run tv viewer.
import os
import sys
from PyQt5 import QtCore, QtWidgets

# my modules
from tv_api_work import tv_api_work as myApi
from tv_sqllite import tv_sqllite as mySql
from logger_conf import logger_conf as myLog

# ===================GLOBALS======================================


# setup logging

logger = myLog.my_logging(__name__)


# ===================CLASSES & FUNCTION SECTION===============================


class Ui_MainWindow(object):
    def __init__(self):
        self.ScreenStatus = 0
        # define instance of the API class
        self.myTvApi = myApi.TvApi("myapiobject")
        # define instance of the SQl class
        self.myTvSql = mySql.TvSqLight("mysqlobject")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Buttons
        self.OneBtn = QtWidgets.QPushButton(self.centralwidget)
        self.OneBtn.setGeometry(QtCore.QRect(20, 600, 100, 30))
        self.OneBtn.setObjectName("OneBtn")
        self.TwoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.TwoBtn.setGeometry(QtCore.QRect(140, 600, 100, 30))
        self.TwoBtn.setObjectName("TwoBtn")
        self.ThreeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ThreeBtn.setGeometry(QtCore.QRect(260, 600, 100, 30))
        self.ThreeBtn.setObjectName("ThreeBtn")
        self.FourBtn = QtWidgets.QPushButton(self.centralwidget)
        self.FourBtn.setGeometry(QtCore.QRect(380, 600, 100, 30))
        self.FourBtn.setObjectName("FourBtn")
        self.FiveBtn = QtWidgets.QPushButton(self.centralwidget)
        self.FiveBtn.setGeometry(QtCore.QRect(500, 600, 100, 30))
        self.FiveBtn.setObjectName("FiveBtn")
        self.ResetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ResetBtn.setGeometry(QtCore.QRect(620, 600, 100, 30))
        self.ResetBtn.setObjectName("Reset")
        self.ExitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ExitBtn.setGeometry(QtCore.QRect(740, 600, 100, 30))
        self.ExitBtn.setObjectName("Exit")

        # radio buttons
        self.OverviewRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.OverviewRbtn.setGeometry(QtCore.QRect(970, 30, 136, 27))
        self.OverviewRbtn.setObjectName("OverviewRbtn")
        self.ActorsRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.ActorsRbtn.setGeometry(QtCore.QRect(970, 80, 136, 27))
        self.ActorsRbtn.setObjectName("ActorsRbtn")
        self.seasonRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.seasonRbtn.setGeometry(QtCore.QRect(970, 130, 136, 27))
        self.seasonRbtn.setObjectName("seasonRbtn")
        self.crewsRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.crewsRbtn.setGeometry(QtCore.QRect(970, 180, 136, 27))
        self.crewsRbtn.setObjectName("crewsRbtn")
        self.infoRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.infoRbtn.setGeometry(QtCore.QRect(970, 230, 136, 27))
        self.infoRbtn.setObjectName("infoRbtn")
        self.episodeRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.episodeRbtn.setGeometry(QtCore.QRect(970, 280, 136, 27))
        self.episodeRbtn.setObjectName("episodeRbtn")

        # List box
        self.listinfo = QtWidgets.QListWidget(self.centralwidget)
        self.listinfo.setGeometry(QtCore.QRect(20, 30, 940, 505))
        self.listinfo.setObjectName("listinfo")
        self.listinfo.setWordWrap(True)
        self.listinfo.setProperty("isWrapping", False)
        self.listinfo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listinfo.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listinfo.setMovement(QtWidgets.QListView.Static)


        # text box
        self.textEnter = QtWidgets.QLineEdit(self.centralwidget)
        self.textEnter.setGeometry(QtCore.QRect(20, 560, 820, 32))
        self.textEnter.setObjectName("textEnter")

        # labels
        self.mainlbl = QtWidgets.QLabel(self.centralwidget)
        self.mainlbl.setGeometry(QtCore.QRect(20, 5, 301, 22))
        self.mainlbl.setObjectName("mainlbl")
        self.txtlbl = QtWidgets.QLabel(self.centralwidget)
        self.txtlbl.setGeometry(QtCore.QRect(20, 535, 90, 22))
        self.txtlbl.setObjectName("txtlbl")
        MainWindow.setCentralWidget(self.centralwidget)

        # menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # add action to menus
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionHelp)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tv Viewer"))

        # Buttons
        self.OneBtn.setText(_translate("MainWindow", "Enter"))
        self.OneBtn.clicked.connect(self.one_button_click)

        self.TwoBtn.setText(_translate("MainWindow", "Select"))
        self.TwoBtn.setEnabled(False)
        self.TwoBtn.clicked.connect(self.two_button_click)

        self.ThreeBtn.setText(_translate("MainWindow", "Upcoming"))
        self.ThreeBtn.clicked.connect(self.three_button_click)
        self.ThreeBtn.setEnabled(False)

        self.FourBtn.setText(_translate("MainWindow", "View Favs"))
        self.FourBtn.clicked.connect(self.four_button_click)

        self.FiveBtn.setText(_translate("MainWindow", "Edit Favs"))
        self.FiveBtn.clicked.connect(self.five_button_click)
        self.FiveBtn.setEnabled(False)

        self.ResetBtn.setText(_translate("MainWindow", "Reset"))
        self.ResetBtn.clicked.connect(self.reset_screen)

        self.ExitBtn.setText(_translate("MainWindow", "Exit"))
        self.ExitBtn.clicked.connect(self.close_application)

        # labels
        self.mainlbl.setText(_translate("MainWindow", "Information Display"))
        self.txtlbl.setText(_translate("MainWindow", "Input Box"))

        # Menubar events
        self.menuFile.setTitle(_translate("MainWindow", "Menu"))
        # about
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut("Ctrl+A")
        self.actionAbout.setStatusTip('App info')
        self.actionAbout.triggered.connect(self.display_about)
        # help menu item
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionHelp.setShortcut("Ctrl+H")
        self.actionHelp.setStatusTip('Display The Help')
        self.actionHelp.triggered.connect(self.display_help)
        # exit menu item
        self.actionExit.setText(_translate("MainWindow", "&Exit"))
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setStatusTip('Leave The App')
        self.actionExit.triggered.connect(self.close_application)

        # radio buttons
        self.OverviewRbtn.setText(_translate("MainWindow", "Overview"))
        self.ActorsRbtn.setText(_translate("MainWindow", "Actors"))
        self.seasonRbtn.setText(_translate("MainWindow", "Seasons"))
        self.crewsRbtn.setText(_translate("MainWindow", "Crews"))
        self.infoRbtn.setText(_translate("MainWindow", "More Info"))
        self.episodeRbtn.setText(_translate("MainWindow", "Episodes"))

        # initialise screen
        self.start_screen()

        # create the database
        self.myTvSql.create_db()



    def close_application(self):
        """ Method control exit of program on exit button click closes database"""
        self.myTvSql.close_db()
        logger.info(' Program Exiting ')
        sys.exit()

    def display_help(self):
        """ Method to display about information on menubar about click"""
        self.listinfo.clear()
        self.listinfo.addItem("\n Readme at :- \
                               \n /usr/share/doc/tv_viewer/\
                               \n or\
                               \n https://github.com/gavinlyonsrepo/tv_viewer")

    def display_about(self):
        """ Method to display about information on menubar help click"""
        self.listinfo.clear()
        self.listinfo.addItem("\n GUI program to view tv program details using tvmaze API \
                               \n Version 1.1 \
                               \n Copyright Gavin Lyons 2017 GPL \
                               \n glyons66@hotmail.com \
                               \n https://github.com/gavinlyonsrepo/tv_viewer \
                               \n Using Python 3.6.0, PyQt5, pytvmaze, sqllite3, prettytable")

    def reset_screen(self):
        """ reset button clicked"""
        self.ScreenStatus = 0
        self.listinfo.clear()
        self.textEnter.clear()
        self.mainlbl.setText("Information Display")
        self.OneBtn.setEnabled(True)
        self.TwoBtn.setEnabled(False)
        self.FourBtn.setEnabled(True)
        self.FiveBtn.setEnabled(False)
        self.start_screen()

    def start_screen(self):
        """initialise start screen list box"""
        self.listinfo.addItem("Welcome: ")
        self.listinfo.addItem("\nWrite a tv show name in Input box and then press Enter to search Tv Series")
        self.listinfo.addItem("\nPress View Favs for Favourites")
        self.listinfo.addItem("\nPress Reset to reset screen")

    def one_button_click(self):
        """ button one ENTER clicked method"""
        self.FourBtn.setEnabled(False)
        # Search show, screenstatus =0, by inputing text
        if self.ScreenStatus == 0:
            if self.textEnter.text():
                self.listinfo.clear()
                items = self.myTvApi.search_tv_series(self.textEnter.text())
                if not items:
                    self.listinfo.addItem("There Is No Matching Tv Show :-")
                else:
                    items = str(items)
                    self.listinfo.addItem(items)
                    self.textEnter.clear()
                    self.ScreenStatus = 1
                    self.listinfo.addItem("To pick a show, enter a row Number in Input Box and press Enter button :-")
                    self.mainlbl.setText("TV show selection screen")
                    return
            else:
                self.listinfo.addItem("Enter a TV show name in Input Box and press Enter button :-")

        # pick show, screenstatus 1, by selecting row number
        if self.ScreenStatus == 1:
            if self.textEnter.text():
                # get tv show
                items = self.myTvApi.show_tv_series(self.textEnter.text())
                if not items:
                    self.listinfo.addItem("Pick a correct row number :-")
                else:
                    self.listinfo.clear()
                    self.listinfo.addItem(str(items))
                    self.OneBtn.setEnabled(False)
                    self.TwoBtn.setEnabled(True)
                    self.FiveBtn.setEnabled(True)
                    self.mainlbl.setText("Tv show information screen")
                    self.listinfo.addItem("Pick an information option on right and then press Select :-")
                    self.listinfo.addItem("You can also toggle Favorite status by entering maze_id in "
                                          "in the Input  box and pressing Edit Favs :-")
            else:
                self.listinfo.addItem("Enter a row Number in Input Box and press Enter Button :-")

        return

    def two_button_click(self):
        """ method to control button 2 SELECT click"""
        self.textEnter.clear()
        self.listinfo.clear()
        self.FiveBtn.setEnabled(False)
        # Scan radio buttons to see if selected run the function for that selection
        # pass the row no of table to relevant TvApi function so it knows show
        if self.OverviewRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.overview(1)))
        elif self.ActorsRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.actors(0)))
        elif self.seasonRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.seasons(0)))
        elif self.crewsRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.crews(0)))
        elif self.infoRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.more_info(1)))
        elif self.episodeRbtn.isChecked():
            self.listinfo.addItem(str(self.myTvApi.episode(0)))
        else:
            self.listinfo.addItem("Select an option from side bar:-")

    def three_button_click(self):
        """ method to control button 3 UPCOMING click """
        # TODO
        self.textEnter.clear()
        self.listinfo.clear()
        self.listinfo.addItem("This functionality not available yet :-")

    def four_button_click(self):
        """ method to control button 4 FAVOURITES click """
        self.FiveBtn.setEnabled(True)
        self.FourBtn.setEnabled(False)
        self.OneBtn.setEnabled(False)
        self.listinfo.clear()
        self.ScreenStatus = 0
        items = self.myTvApi.favour_show(self.myTvSql.display_db())
        self.listinfo.addItem(str(items))
        self.listinfo.addItem("Enter a maze_ID and press Edit Favs button, If present in database")
        self.listinfo.addItem("it will be Deleted, if not present it will be added :- ")
        self.mainlbl.setText("Favourites Information Screen")

    def five_button_click(self):
        """ method to control button 5 EDIT FAVS click"""
        self.OneBtn.setEnabled(False)
        self.TwoBtn.setEnabled(False)
        mazeid = self.textEnter.text()
        if mazeid:
            # check if in database
            showflag = self.myTvSql.scan_db(mazeid)
            if showflag:
                # True delete if in database
                self.myTvSql.del_db(mazeid)
                self.four_button_click()
                self.listinfo.addItem("Removed maze_id {} from the database:-".format(mazeid))
            else:
                # False add if not in database
                # check here if valid maze ID from API
                name = self.myTvApi.showname_get(mazeid)
                if name != "Error":
                    self.myTvSql.add_db(mazeid, name)
                    self.four_button_click()
                    self.listinfo.addItem("Added maze_id {} to the database:-".format(mazeid))
                else:
                    self.listinfo.addItem("Cannot find that Maze_ID with API :-")
        else:
            self.listinfo.addItem("Add a Maze_Id and press again :-")


# =====================MAIN===============================
def test(text):
    """ Test module imported function """
    logger.info(text)


if __name__ == '__main__':
    test("main")
else:
    test(" Imported {}".format(__name__))
# =====================END===============================
