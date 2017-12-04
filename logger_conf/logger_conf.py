#!/usr/bin/env python3
"""logger_conf.py module used by tv_viewer program, imported into modules sets up logging"""


# ==========================IMPORTS======================
# Import the system modules needed to run 
import logging 

# ====================FUNCTION SECTION===============================


def my_logging(module_name):

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('/tmp/tv_viewer.log')
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
