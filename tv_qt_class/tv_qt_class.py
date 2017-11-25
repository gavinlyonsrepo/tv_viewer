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
# main api:         :http://www.tvmaze.com/api
# second api:       :https://www.episodate.com/api

#==========================IMPORTS======================
# Import the system modules needed to run tv viewer.
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#my modules
import tv_api_work
import tv_sqllite

# ======================GLOBALS=========================
myTvApi = tv_api_work.Tvapi("Apiclsobj1")

# path for db to hold favs
DESTCONFIG = os.environ['HOME'] + "/.config/tv_viewer"
if not os.path.exists(DESTCONFIG):
    os.makedirs(DESTCONFIG)

myTvSql = tv_sqllite.TvSqLight("Sqlclsobj1", DESTCONFIG + "/" + "fav.db")

if not myTvSql.create_db():
    #error
    pass

# ===================FUNCTION SECTION===============================


class Ui_MainWindow(object):

    def __init__(self):
        self.ScreenStatus = 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(896, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Buttons
        self.OneBtn = QtWidgets.QPushButton(self.centralwidget)
        self.OneBtn.setGeometry(QtCore.QRect(20, 500, 100, 30))
        self.OneBtn.setObjectName("OneBtn")
        self.TwoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.TwoBtn.setGeometry(QtCore.QRect(140, 500, 100, 30))
        self.TwoBtn.setObjectName("TwoBtn")
        self.ThreeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ThreeBtn.setGeometry(QtCore.QRect(260, 500, 100, 30))
        self.ThreeBtn.setObjectName("ThreeBtn")
        self.FourBtn = QtWidgets.QPushButton(self.centralwidget)
        self.FourBtn.setGeometry(QtCore.QRect(380, 500, 100, 30))
        self.FourBtn.setObjectName("FourBtn")
        self.FiveBtn = QtWidgets.QPushButton(self.centralwidget)
        self.FiveBtn.setGeometry(QtCore.QRect(500, 500, 100, 30))
        self.FiveBtn.setObjectName("FiveBtn")
        self.ResetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ResetBtn.setGeometry(QtCore.QRect(620, 500, 100, 30))
        self.ResetBtn.setObjectName("Reset")
        self.ExitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ExitBtn.setGeometry(QtCore.QRect(740, 500, 100, 30))
        self.ExitBtn.setObjectName("Exit")

        # radio buttons
        self.OverviewRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.OverviewRbtn.setGeometry(QtCore.QRect(750, 50, 136, 27))
        self.OverviewRbtn.setObjectName("OverviewRbtn")
        self.ActorsRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.ActorsRbtn.setGeometry(QtCore.QRect(750, 100, 136, 27))
        self.ActorsRbtn.setObjectName("ActorsRbtn")
        self.seaepiBtn = QtWidgets.QRadioButton(self.centralwidget)
        self.seaepiBtn.setGeometry(QtCore.QRect(750, 160, 136, 27))
        self.seaepiBtn.setObjectName("seaepiBtn")
        self.crewsRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.crewsRbtn.setGeometry(QtCore.QRect(750, 220, 136, 27))
        self.crewsRbtn.setObjectName("crewsRbtn")
        self.infoRbtn = QtWidgets.QRadioButton(self.centralwidget)
        self.infoRbtn.setGeometry(QtCore.QRect(750, 280, 136, 27))
        self.infoRbtn.setObjectName("infoRbtn")

        # List box
        self.listinfo = QtWidgets.QListWidget(self.centralwidget)
        self.listinfo.setGeometry(QtCore.QRect(20, 30, 721, 381))
        self.listinfo.setObjectName("listinfo")

        # text box
        self.textEnter = QtWidgets.QLineEdit(self.centralwidget)
        self.textEnter.setGeometry(QtCore.QRect(20, 450, 721, 32))
        self.textEnter.setObjectName("textEnter")

        # labels
        self.mainlbl = QtWidgets.QLabel(self.centralwidget)
        self.mainlbl.setGeometry(QtCore.QRect(20, 5, 301, 22))
        self.mainlbl.setObjectName("mainlbl")
        self.txtlbl = QtWidgets.QLabel(self.centralwidget)
        self.txtlbl.setGeometry(QtCore.QRect(20, 425, 79, 22))
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
        self.OneBtn.clicked.connect(self.OneButton_click)

        self.TwoBtn.setText(_translate("MainWindow", "Select"))
        self.TwoBtn.setEnabled(False)
        self.TwoBtn.clicked.connect(self.TwoButton_click)

        self.ThreeBtn.setText(_translate("MainWindow", "Upcoming"))
        self.ThreeBtn.clicked.connect(self.ThreeButton_click)
        self.ThreeBtn.setEnabled(False)

        self.FourBtn.setText(_translate("MainWindow", "View Favs"))
        self.FourBtn.clicked.connect(self.FourButton_click)

        self.FiveBtn.setText(_translate("MainWindow", "Edit Favs"))
        self.FiveBtn.clicked.connect(self.FiveButton_click)

        self.ResetBtn.setText(_translate("MainWindow", "Reset"))
        self.ResetBtn.clicked.connect(self.reset_screen)

        self.ExitBtn.setText(_translate("MainWindow", "Exit"))
        self.ExitBtn.clicked.connect(self.close_application)
        # labels
        self.mainlbl.setText(_translate("MainWindow", "Information"))
        self.txtlbl.setText(_translate("MainWindow", "Input"))

        # Menubar events
        self.menuFile.setTitle(_translate("MainWindow", "Misc"))
        # about
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut("Ctrl+A")
        self.actionAbout.setStatusTip('App info')
        self.actionAbout.triggered.connect(self.display_about)
        # help menuitem
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
        self.seaepiBtn.setText(_translate("MainWindow", "Season / epi"))
        self.crewsRbtn.setText(_translate("MainWindow", "Crews"))
        self.infoRbtn.setText(_translate("MainWindow", "More Info"))
        self.OverviewRbtn.setEnabled(False)
        self.ActorsRbtn.setEnabled(False)
        self.seaepiBtn.setEnabled(False)
        self.crewsRbtn.setEnabled(False)
        self.infoRbtn.setEnabled(False)

        # initalise listbox
        self.start_screen()

    def close_application(self):
        print("Goodbye Exit")
        myTvSql.close_db()
        sys.exit()

    def display_help(self):
        self.listinfo.clear()
        self.listinfo.addItem("help")
        print("This is the help")

    def display_about(self):
        self.listinfo.clear()
        self.listinfo.addItem("about")
        print("This is the about")

    def reset_screen(self):
        """ reset button clicked"""
        self.ScreenStatus = 0
        self.listinfo.clear()
        self.textEnter.clear()
        self.start_screen()

    def start_screen(self):
        """initialise start screen list box"""
        self.listinfo.addItem("Welcome: ")
        self.listinfo.addItem("Press Enter to search Tv Series")
        self.listinfo.addItem("Press View Fav for Favourites")
        self.listinfo.addItem("Press Reset to Reset screen")

    def OneButton_click(self):
        """ button one clicked """

        # Search screen status 0
        if self.ScreenStatus == 0:
            if self.textEnter.text():
                self.listinfo.clear()
                items = myTvApi.searchTvSeries(self.textEnter.text())
                if not items:
                    self.listinfo.addItem("There Is No Matching Tv Show")
                else:
                    items = str(items)
                    self.listinfo.addItem(items)
                    self.textEnter.clear()
                    self.ScreenStatus = 1
                    #self.listinfo.additem(":")
                    self.listinfo.addItem("Enter a row Number in Input Box and press Enter button")
                    return
            else:
                #self.listinfo.additem(":")
                self.listinfo.addItem("Enter a TV show in Input Box and press Enter button")

        # pick show status 1
        if self.ScreenStatus == 1:
            if self.textEnter.text():
                # get tv show
                items = myTvApi.showTvSeries(self.textEnter.text())
                if not items:
                    self.listinfo.addItem("Pick a correct row number")
                else:
                    self.listinfo.clear()
                    self.listinfo.addItem(str(items))
            else:
               # self.listinfo.additem(" ")
                self.listinfo.addItem("Enter a row Number in Input Box and press Enter Button")

        return

    def TwoButton_click(self):
        """ button 2 clicked """
        self.textEnter.clear()
        self.listinfo.clear()
        self.listinfo.addItem("This functionality not available yet")

    def ThreeButton_click(self):
        """ button 3 clicked """
        self.textEnter.clear()
        self.listinfo.clear()
        self.listinfo.addItem("This functionality not available yet")

    def FourButton_click(self):
        """ button 4 clicked """
        self.listinfo.clear()
        self.ScreenStatus = 0
        items = myTvApi.favour_show(myTvSql.display_db())
        self.listinfo.addItem(str(items))
        self.listinfo.addItem("To delete a Fav from database enter a existing maze_ID and press Fav edit")
        self.listinfo.addItem("To add a Fav to database enter a maze_ID of tv show and press Fav edit")

    def FiveButton_click(self):
        """ button 5 clicked """
        mazeid = self.textEnter.text()
        if mazeid:
            showflag = myTvSql.scan_db(mazeid)
            print(showflag)
            if showflag:
                # delete if in database
                myTvSql.delrec_db(mazeid)
                self.FourButton_click()
            else:
                # add if not in database
                name = myTvApi.showname_get(mazeid)
                myTvSql.addrec_db(mazeid, name)
                self.FourButton_click()
        else:
            self.listinfo.addItem("Add a Maze_Id and press again")


# =====================MAIN===============================
def test(text):
    """ docstring """
    print(text)
    pass

if __name__ == '__main__':
    test("main")
else:
    test("Imported {}".format(__name__))
# =====================END===============================
