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
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#my modules
import tv_api_work


# ======================GLOBALS=========================
myTV = tv_api_work.Tvapi("Gavin")

# ===================FUNCTION SECTION===============================


class Ui_MainWindow(object):

    def __init__(self):
        self.ScreenStatus = 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Buttons
        self.OneBtn = QtWidgets.QPushButton(self.centralwidget)
        self.OneBtn.setGeometry(QtCore.QRect(20, 500, 115, 30))
        self.OneBtn.setObjectName("OneBtn")
        self.TwoBtn = QtWidgets.QPushButton(self.centralwidget)
        self.TwoBtn.setGeometry(QtCore.QRect(180, 500, 115, 30))
        self.TwoBtn.setObjectName("TwoBtn")
        self.ThreeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ThreeBtn.setGeometry(QtCore.QRect(340, 500, 115, 30))
        self.ThreeBtn.setObjectName("ThreeBtn")
        self.ResetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ResetBtn.setGeometry(QtCore.QRect(500, 500, 115, 30))
        self.ResetBtn.setObjectName("Reset")

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
        self.mainlbl.setGeometry(QtCore.QRect(20, 10, 301, 22))
        self.mainlbl.setObjectName("mainlbl")
        self.txtlbl = QtWidgets.QLabel(self.centralwidget)
        self.txtlbl.setGeometry(QtCore.QRect(20, 430, 79, 22))
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
        self.OneBtn.setText(_translate("MainWindow", "One "))
        self.OneBtn.clicked.connect(self.OneButton_click)

        self.TwoBtn.setText(_translate("MainWindow", "Two"))
        self.TwoBtn.clicked.connect(self.TwoButton_click)

        self.ThreeBtn.setText(_translate("MainWindow", "Three"))
        self.ThreeBtn.clicked.connect(self.ThreeButton_click)

        self.ResetBtn.setText(_translate("MainWindow", "Reset"))
        self.ResetBtn.clicked.connect(self.reset_screen)

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

        # initalise listbox

        self.start_screen()

    def close_application(self):
        print("Goodbye Exit")
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
        self.listinfo.addItem("Press One to search Tv Series")
        self.listinfo.addItem("Press Two for Favourites")
        self.listinfo.addItem("Press Three for Up-Coming Tv Show's")



    def OneButton_click(self):
        """ button one clicked """

        # Search screen status 0
        if self.ScreenStatus == 0:
            if self.textEnter.text():
                self.listinfo.clear()
                items = myTV.searchTvSeries(self.textEnter.text())
                # print(items)
                if not items:
                    self.listinfo.addItem("There Is No Matching Tv Show")
                else:
                    items = str(items)
                    self.listinfo.addItem(items)
                    self.textEnter.clear()
                    self.ScreenStatus = 1
                    self.listinfo.addItem("Enter a row Number in Input Box and press one")
                    return
            else:
                self.listinfo.addItem("Enter a TV show in Input Box and press one")

        # pick show status 1
        if self.ScreenStatus == 1:
           if self.textEnter.text():
                #get tv show
                items = myTV.showTvSeries(self.textEnter.text())
                # print(myTV.tvshowtable)
                self.listinfo.clear()
                self.listinfo.addItem(items)
           else:
               self.listinfo.addItem("Enter a row Number in Input Box")

        return

    def TwoButton_click(self):
        """ button 3 clicked """
        if self.ScreenStatus == 0:
            print("button two")
            self.listinfo.addItem("This functionality not available yet")

    def ThreeButton_click(self):
        """ button 3 clicked """
        if self.ScreenStatus == 0:
            self.listinfo.addItem("This functionality not available yet")





# =====================MAIN===============================
def test(text):
    """ docstring """
    print(text)
    pass

if __name__ == '__main__':
    test("main")
else:
    test("Imported tv_qt_class")
# =====================END===============================
