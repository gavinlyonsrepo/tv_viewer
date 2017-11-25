#!/usr/bin/env python3
""" tv_viewer : Python PyQt5 GUI to view tv program details using tvmaze API """
# =========================HEADER=======================================
# author            :Gavin Lyons
# title             :tv_viewer
# description       :Python PyQt5 GUI to view tv program details using tvmaze API
# author            :Gavin Lyons
# date              :20/08/2017
# version           :0.1.0
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# mail              :glyons66@hotmail.com
# python_version    :3.6.0


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
    app.setWindowIcon(QIcon('/home/gavin/Documents/Tech/Linux/python/tv_viewer/desktop/tv_viewer.png'))
    Myqt.MainWindow = QtWidgets.QMainWindow()
    ui = Myqt()
    ui.setupUi(Myqt.MainWindow)
    Myqt.MainWindow.show()
    sys.exit(app.exec_())
# =====================END===============================
