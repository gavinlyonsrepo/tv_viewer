#!/usr/bin/env python3
"""tv_sqllite.py  """
# =========================HEADER=======================================
# title             :tv_sqllite.py
# description       :This module is called from tv_viewer.py to handle Sqlite interaction
# author            :Gavin Lyons
# date              :24/11/2017
# web               :https://github.com/gavinlyonsrepo/
# mail              :glyons66@hotmail.com
# python_version    :

# ==========================IMPORTS======================
# Import the system modules needed to run 
import sqlite3

# my modules



# =======================GLOBALS=========================


# ====================class sectionFUNCTION SECTION===============================

class TvSqLight(object):

    def __init__(self, name, path):
        self.name = name
        self.connection = ""
        self.path = path

    def create_db(self):
        try:
            conn = sqlite3.connect(self.path)
            self.connection = conn.cursor()
            self.connection.execute("""CREATE TABLE IF NOT EXISTS shows (
                    number integer,
                    name text
                    )""")
        except Exception as error4:
            print(error4)
        return

    def scan_db(self, mazeid):
        """Method to scan scan database for an ID return true if it exists False if not"""
        flag = True
        conn = sqlite3.connect(self.path)
        self.connection = conn.cursor()
        self.connection.execute("SELECT * FROM shows WHERE number=:number", {'number': mazeid})
        if not self.connection.fetchall():
            # empty list if not in database
            flag = False
        return flag

    def display_db(self):
        conn = sqlite3.connect(self.path)
        self.connection = conn.cursor()
        self.connection.execute("SELECT * FROM shows")
        return self.connection.fetchall()

    def addrec_db(self, mazeid, showname):
        conn = sqlite3.connect(self.path)
        self.connection = conn.cursor()
        with conn:
            self.connection.execute("INSERT INTO shows VALUES (:number, :name)", {'number': mazeid, 'name': str(showname)})
        return

    def delrec_db(self, mazeid):
        conn = sqlite3.connect(self.path)
        self.connection = conn.cursor()
        with conn:
            self.connection.execute("DELETE FROM shows WHERE number=:number", {'number': mazeid})
        return

    def close_db(self):
        conn = sqlite3.connect(self.path)
        self.connection = conn.cursor()
        self.connection.close()

# =====================MAIN===============================
def test(text):
    """ testing function 1"""
    print(text)


if __name__ == '__main__':
    test("main")
else:
    test("Imported {}".format(__name__))
# =====================END===============================
