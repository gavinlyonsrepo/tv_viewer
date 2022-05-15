#!/usr/bin/env python3
""" This module is called from tv_viewer.py to handle Sqllite
database interaction, contains one class TvSqLight , 6 methods"""
# =========================MODULE HEADER=======================================
# title             :tv_sqllite.py
# description       :This module from tv_viewer to handle Sqlite interaction
# author            :Gavin Lyons
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# python_version    :3.10.4

# ==========================IMPORTS======================
# Import the system modules needed to run
import os
import sqlite3

from tv_logger_conf import tv_logger_conf as my_log

# ====================== GLOBALS =======================
# setup logging
logger = my_log.my_logging(__name__)

# ====================CLASS SECTION===============================


class TvSqLight:
    """class to interact with sqlite database
    contains 6 methods, create close
    the database. add, delete, scan, and display data.
    object is initialise with a path"""

    def __init__(self, name):
        self.name = name
        self.connection = ""
        if not os.path.exists(my_log.myconfigfile.config_file_path):
            os.makedirs(my_log.myconfigfile.config_file_path)
        self.path = my_log.myconfigfile.config_file_path / "fav.db"

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
            logger.exception(" Failed to Create user database: ")

    def scan_db(self, mazeid):
        """Method to scan database for an ID,
        return true if it exists, False if not"""
        try:
            flag = True
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.execute(
                "SELECT * FROM shows WHERE number=:number", {'number': mazeid})
            if not self.connection.fetchall():  # empty list if not in database
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
        """ method to add record to database
        called by Fav add button"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            with conn:
                self.connection.execute(
                    "INSERT INTO shows VALUES (:number, :name)",
                    {'number': mazeid, 'name': str(showname)})
        except sqlite3.Error:
            logger.exception(" Failed to Add record database :: %s ", mazeid)

    def del_db(self, maze_id):
        """ method to delete record to database
        called by Fav del button"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            with conn:
                self.connection.execute(
                    "DELETE FROM shows WHERE number=:number",
                    {'number': maze_id})
        except sqlite3.Error:
            logger.exception(" Failed to remove record database: %s", maze_id)

    def close_db(self):
        """method to close database connection at end of program"""
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.close()
        except sqlite3.Error:
            logger.exception(" Failed to close user database : : ")

# =====================MAIN===============================


def test(text):
    """ testing imported """
    logger.info(text)


if __name__ == '__main__':
    test(" main")
else:
    test(" Imported " + __name__)
# =====================END===============================
