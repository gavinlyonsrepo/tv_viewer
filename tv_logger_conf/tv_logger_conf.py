#!/usr/bin/env python3
"""
filename:    tv_logger_conf.py
description:Module to setup logging ,config file handling  and
    installation of desktop entry files. 
    imported into modules sets up logging, config file
"""
# Import the system modules needed to run
import logging
import os
import sys
import datetime
import configparser
from pathlib import Path
import subprocess


# ====================FUNCTION SECTION====================

class Settings:
    """Singleton class to manage application settings."""

    CONFIG_PATH = Path.home() / ".config" / "tv_viewer" / "tvviewer_v3.cfg"
    LOG_PATH = Path.home() / ".cache" / "tv_viewer"
    DEFAULTS = {
        "Debug":   {"debugOnOff": "0"},
        "Display": {"screen_resolution": "1100x800", "font_size": 11, "font_name": "Courier"},
        "Logging": {"logging_dir": LOG_PATH, "loggingOnOff": "0"},
        "Network": {"mazetv_url": "www.tvmaze.com", "NetworkCheckOnOff": "1"},
    }

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load()

    def load(self):
        """ Function to load the config file, if missing settings 
        puts them , if file missing creates it."""
        if self.CONFIG_PATH.exists():
            self.config.read(self.CONFIG_PATH)
        for section, defaults in self.DEFAULTS.items():
            if section not in self.config:
                self.config[section] = defaults.copy()
            else:
                for key, val in defaults.items():
                    self.config[section].setdefault(key, val)
        if not self.CONFIG_PATH.exists():
            self.save()

    def save(self):
        """ Function if config file does not exist 
        create , fill with defaults"""
        self.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with self.CONFIG_PATH.open("w", encoding="utf-8") as f:
            self.config.write(f)

    def getint(self, section, option, fallback):
        """Get an integer setting with a fallback value."""
        return self.config.getint(section, option, fallback=fallback)

    def getbool(self, section, option, fallback=False):
        """Get a boolean setting (0/1 or true/false)."""
        return self.config.getboolean(section, option, fallback=fallback)

    def getstr(self, section, option, fallback=""):
        """Get a string setting with a fallback value."""
        return self.config.get(section, option, fallback=fallback)

    def set(self, section, option, value):
        """Set a config value and save."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = str(value)
        self.save()


def my_logging(module_name):
    """Function to carry out logging"""
    log_file_path = Path(settings.getstr("Logging", "logging_dir", fallback=str("/tmp")))
    logging_on_off = settings.getbool("Logging", "loggingOnOff", fallback=0)
    log_file_path.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    if logging_on_off == 1:
        basename = "TVviewer"
        suffix = datetime.datetime.now().strftime("%d%m%y_%H%M%S" + ".log")
        # e.g. filename = 'TVviewer_120508_171442.log'
        filename = "_".join([basename, suffix])
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(log_file_path / filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    elif logging_on_off == 0:
        logger.disabled = True

    return logger

def install_desktop_entry():
    """ Downloads the desktop icon and entry file from github 
    and installs them to coorect location"""
    messages = []
    try:
        if not sys.platform.startswith("linux"):
            messages.append("Desktop entry installation is Linux only.")
            return False, messages
        path_list = [os.environ['HOME'] + "/.local/share/icons/",
                    os.environ['HOME'] + "/.local/share/applications/"]
        github_list = [
            'https://raw.githubusercontent.com/gavinlyonsrepo/'
            'tv_viewer/master/desktop/tv_viewer.png',
            'https://raw.githubusercontent.com/gavinlyonsrepo/'
            'tv_viewer/master/desktop/tv_viewer.desktop'
        ]
        file_list = ['tv_viewer.png', 'tv_viewer.desktop']
        for (my_file, my_path, my_github_url) in zip(file_list, path_list, github_list):
            if not os.path.exists(my_path):
                os.makedirs(my_path)
            if not os.path.isfile(my_path + '/' + my_file):
                os.chdir(my_path)
                result = subprocess.run(['curl', '-s', '--fail', '-o',
                                          my_file, my_github_url], check=True)
                if result.returncode != 0:
                    raise RuntimeError(f"curl failed downloading {my_file}")
                messages.append(f"{my_file} installed in {my_path}")
            else:
                messages.append(f"{my_file} at {my_path} already exists")
        return True, messages
    except Exception as error: # pylint: disable=broad-exception-caught)
        messages.append("INFO 1202 :: Downloading desktop entry/icon from github")
        messages.append("Failed. Github or network may be down or Curl not installed")
        messages.append(f"Error :: {error}")
        return False, messages

# =====================MAIN===============================
# create settings instance singleton.
settings = Settings()

def start(text):
    """ Starts logging """
    logger = my_logging(__name__)
    logger.info(text)


if __name__ == '__main__':
    start("main")
else:
    start(" Imported " + __name__)
# =====================END===============================
