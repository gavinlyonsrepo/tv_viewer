#!/usr/bin/env python3
"""tv_logger_conf.py module used by tv_viewer program,
imported into modules sets up logging and config file"""
# ======================== FILE HEADER =================
# title             :tv_logger.conf
# description       :Module to setup logging and config file handling
# author            :Gavin Lyons
# version           :2.0
# web               :https://github.com/gavinlyonsrepo/tv_viewer
# python_version    :3.10.4

# ==========================IMPORTS======================
# Import the system modules needed to run
import logging
import os
import sys
import datetime
import configparser
from pathlib import Path


# ====================FUNCTION SECTION====================
class TvConfigFile:
    """Class to handle config file reading
    and creation, called before logging"""
    def __init__(self, name):
        self.name = name
        self.logging_on_off = "off"
        if sys.platform == 'win32':
            home_path = os.environ['HOMEPATH']
        else:
            home_path = os.environ['HOME']
        self.log_file = Path(home_path + "/.cache/tv_viewer")
        self.config_file_path = Path(home_path + "/.config/tv_viewer")
        self.network_on_off = 'on'
        self.network_url = 'www.tvmaze.com'

    def create_configfile_func(self):
        """ creates a config file with default values if missing"""
        # Check config path is there
        if not os.path.exists(self.config_file_path):
            os.makedirs(self.config_file_path)
        config_file_path = self.config_file_path / "tvviewer.cfg"
        if os.path.isfile(config_file_path):  # Check config file is there
            pass  # Configfile is there
        else:
            try:  # Create the missing configfile with some defaults
                config = configparser.ConfigParser()
                config['MAIN'] = {'loggingonoff': 'off',
                                  'logpath': self.log_file,
                                  'networkcheckonoff': 'on',
                                  'networkurl': 'www.tvmaze.com'}
                with open(config_file_path, 'w', encoding="utf-8") as configfile:
                    config.write(configfile)
            except Exception as error:
                print("Config file is missing at " + str(config_file_path))
                print("Problem trying to create config file: " + str(error))
            else:
                print("Config file was missing at " + str(config_file_path))
                print("Config file created with default values.")

    def read_configfile_func(self):
        """Read in configfile"""
        try:
            my_config_file = configparser.ConfigParser()
            config_file_path = self.config_file_path / "tvviewer.cfg"
            my_config_file.read(config_file_path)
            self.logging_on_off = my_config_file.get("MAIN", "loggingonoff")
            self.log_file = Path(my_config_file.get("MAIN", "logpath"))
            self.network_on_off = my_config_file.get("MAIN", "networkcheckonoff")
            self.network_url = my_config_file.get("MAIN", "networkurl")
        except Exception as error:
            print(" Problem reading in config file: " + str(error))


def my_logging(module_name):
    """Function to carry out logging"""
    if not os.path.exists(myconfigfile.log_file):
        os.makedirs(myconfigfile.log_file)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    if myconfigfile.logging_on_off == "on":
        basename = "TVviewer"
        suffix = datetime.datetime.now().strftime("%d%m%y_%H%M%S" + ".log")
        # e.g. filename = 'TVviewer_120508_171442.log'
        filename = "_".join([basename, suffix])
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(myconfigfile.log_file / filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    elif myconfigfile.logging_on_off == "off":
        logger.disabled = True

    return logger


# =====================MAIN===============================
myconfigfile = TvConfigFile("objectname")


def start(text):
    """ Sets up config file if not exist , reads it in and starts logging """
    myconfigfile.create_configfile_func()
    myconfigfile.read_configfile_func()
    logger = my_logging(__name__)
    logger.info(text)


if __name__ == '__main__':
    start("main")
else:
    start(" Imported " + __name__)
# =====================END===============================
