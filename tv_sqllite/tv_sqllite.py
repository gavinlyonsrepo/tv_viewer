#!/usr/bin/env python3
""" This module is called from tv_viewer.py to handle Sqllite
database interaction, contains one class TvSqLight , 6 methods"""
# =========================MODULE HEADER=======================================
# title             :tv_sqllite.py
# description       :This module is called from tv_viewer.py to handle Sqlite interaction
# author            :Gavin Lyons
# date              :24/11/2017
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# mail              :glyons66@hotmail.com
# python_version    :3.6.0

# ==========================IMPORTS======================
# Import the system modules needed to run
import os
import sqlite3


from logger_conf import logger_conf as myLog

# ====================== GLOBALS =======================
# setup logging
logger = myLog.my_logging(__name__)
DESTCONFIG = os.environ['HOME'] + "/.config/tv_viewer"
if not os.path.exists(DESTCONFIG):
    os.makedirs(DESTCONFIG)

# ====================CLASS SECTION===============================


class TvSqLight(object):
    """class to interact with sqlite database contains 6 methods, create close
    the database. add, delete, scan, and display data. object is initialise with a path"""
    # path for db to hold favs


    def __init__(self, name):
        self.name = name
        self.connection = ""
        self.path = DESTCONFIG + "/" + "fav.db"

    def create_db(self):
        """ Method to create the database one table two fields"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.execute("""CREATE TABLE IF NOT EXISTS shows (
                    number integer,
                    name text
                    )""")
        except sqlite3.OperationalError:
            logger.exception(" Failed to Create database: ")

    def scan_db(self, mazeid):
        """Method to scan scan database for an ID, return true if it exists, False if not"""
        try:
            flag = True
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.execute("SELECT * FROM shows WHERE number=:number", {'number': mazeid})
            if not self.connection.fetchall():
                # empty list if not in database
                flag = False
        except sqlite3.Error:
            flag = False
            logger.exception(" Failed to Scan database: ")
        return flag

    def display_db(self):
        """ method to display database called from Favs screen"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.execute("SELECT * FROM shows")
        except sqlite3.Error:
            logger.exception(" Failed to Display database: ")
        return self.connection.fetchall()

    def add_db(self, mazeid, showname):
        """ method to add record to database called by Fav edit button"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            with conn:
                self.connection.execute("INSERT INTO shows VALUES (:number, :name)", {'number': mazeid, 'name': str(showname)})
        except sqlite3.Error:
            logger.exception(" Failed to Add record database: ")
        return

    def del_db(self, maze_id):
        """ method to delete record to database called by Fav edit button"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            with conn:
                self.connection.execute("DELETE FROM shows WHERE number=:number", {'number': maze_id})
        except sqlite3.Error:
            logger.exception(" Failed to remove record database: ")
        return

    def close_db(self):
        """method to close database connection at end of program"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.close()
        except sqlite3.Error:
            logger.exception(" Failed to close database: ")
        return
# =====================MAIN===============================


def test(text):
    """ testing imported """
    logger.info(text)


if __name__ == '__main__':
    test(" main")
else:
    test("   Imported {}".format(__name__))
# =====================END===============================
