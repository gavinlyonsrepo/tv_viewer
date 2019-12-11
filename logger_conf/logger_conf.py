#!/usr/bin/env python3
"""logger_conf.py module used by tv_viewer program, imported into modules sets up logging"""


# ==========================IMPORTS======================
# Import the system modules needed to run 
import logging 
import os
import datetime

# ====================FUNCTION SECTION===============================


def my_logging(module_name):
    DESTCACHE = os.environ['HOME'] + "/.cache/tv_viewer"
    if not os.path.exists(DESTCACHE):
        os.makedirs(DESTCACHE)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    basename = "tvviewerlog"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix]) # e.g. 'tvviewer_120508_171442'
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(DESTCACHE + "/" + filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

# =====================MAIN===============================


def test(text):
    """ testing function 1"""
    logger = my_logging(__name__)
    logger.info(text)


if __name__ == '__main__':
    test("main")
else:
    test(" Imported {}".format(__name__))
# =====================END===============================
