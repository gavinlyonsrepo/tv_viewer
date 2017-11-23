#!/usr/bin/env python3
"""python script """
# =========================HEADER=======================================
# title             :tv_viewer
# description       :GUI to view tv program details
# author            :Gavin Lyons
# date              :21/08/2017
# version           :1.0
# web               :https://github.com/gavinlyonsrepo/
# mail              :glyons66@hotmail.com
# python_version    :3.6.0


# ==========================IMPORTS======================
# Import the system modules needed to run 
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

#my modules
from tv_qt_class import Ui_MainWindow as Myqt
# =======================GLOBALS=========================


# ====================FUNCTION SECTION===============================


# =====================MAIN===============================
def test():
    """ docstring """
    print("main")
    pass


if __name__ == "__main__":
    test()

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('/home/gavin/Documents/Tech/Linux/python/tv_viewer/desktop/tv_viewer.png'))
    Myqt.MainWindow = QtWidgets.QMainWindow()
    ui = Myqt()
    ui.setupUi(Myqt.MainWindow)
    Myqt.MainWindow.show()
    sys.exit(app.exec_())
#=====================END===============================
