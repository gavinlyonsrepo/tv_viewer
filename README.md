[![Website](https://img.shields.io/badge/Website-Link-blue.svg)](https://gavinlyonsrepo.github.io/)  [![Rss](https://img.shields.io/badge/Subscribe-RSS-yellow.svg)](https://gavinlyonsrepo.github.io//feed.xml)  [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/whitelight976)


## Overview

* Name: tv_viewer
* Title : Graphical user interface to view TV show details using the TV maze API 
* Description: 

GUI to view details  of tv programs using TV maze application 
programming interface. Written in python 3 and PyQt 5, it also stores 
user favourites in an SQLite database. 
It uses python module pytvmaze to interface with API 
and python module prettytable to help display results.

* [TV maze API](http://www.tvmaze.com/api)

* Author: Gavin Lyons 
* Upstream repository: [Github](https://github.com/gavinlyonsrepo/tv_viewer)
* Developed and tested on Linux as a Linux App. 

## Table of contents

  * [Overview](#overview)
  * [Table of contents](#table-of-contents)
  * [Installation and Setup](#installation-and-setup)
  * [Usage](#usage)
  * [File system](#file-system)
	* [Log file](#log-file)
	* [Configuration file](#configuration-file)  
  * [Dependencies](#dependencies)
  * [Features](#features)
  * [Screenshot](#screenshot)

## Installation and Setup

Latest version 2.3. 

**PyPi & pip , pipx**

The program is present in python package index, Pypi.
Install using *pip* or *pipx* to the location or environment of your choice.


**Arch based Linux distribution**

If you are using an arch Linux based system,
the program is packaged in the AUR as 'tv_viewer'.

**Manually install from github**

The package is also archived on github and can be manually download and installed 
via python and setup.py

```sh
curl -sL https://github.com/gavinlyonsrepo/tv_viewer/archive/2.3.tar.gz | tar xz
cd tv_viewer-2.3
python3 setup.py build 
python3 setup.py install --user
```

## Usage

type below in terminal  to launch *or* select icon from Desktop app menus under Other( Linux only)

```sh
tv_viewer.py 
```

## File system


| File Path | Description |
| ------ | ------ |
| 'HOME'/.config/tv_viewer/fav.db | Favourite Database, created by program on startup |
| 'HOME'/.config/tv_viewer/tvviewer.cfg | config file,  created by program on startup |
| 'HOME'/.cache/tv_viewer/TVviewer_YYMMDD_HHMMSS.log | Log file Path can be adjusted in config |
| 'HOME'/.local/share/icons/tv_viewer.png | icon, Linux only |
| 'HOME'/.local/share/applications/tv_viewer.desktop | desktop entry, Linux only |
| tv_viewer.py | main executable python script |
| tv_qt_class.py | python module dealing with PyQt code |
| tv_sqllite.py | python module dealing with SQLite code |
| tv_api_work.py | python module dealing with Pytvmaze code |
| tv_logger_conf.py | python module dealing with logging and config file |

When the program starts for first time it creates a blank database and a config file  
and  (if installed by pip) downloads from github using curl the two files for the desktop entry and icon.
All files are placed in 'HOME'/.local/* . On Linux systems 'HOME' is defined by os.environ['HOME']
on windows os.environ['HOMEPATH']

### Log file

A debug log file to store information outputted by program. 

```sh
2017-12-04 15:03:32:INFO:__main__:  Main Loop Start
2017-12-04 15:04:42:WARNING:tv_api_work.tv_api_work:No next episode data available
```
Exceptions are generated by software as a result of missing and incomplete 
API data by TV maze for some shows. These are caught and outputted 
to log file and won't interfere with running of program. 
The software should catch most issues 
and output them there. Also displayed here are various other debug information.
Logging can be switched on and off in and the output path  can be changed.

### Configuration file


The configuration file is created on startup and populated by default values

| Setting  | Value |  Default | Note |
| ------ | ------ | ----- | ----- |
| loggingonoff | on or off | off | Toggles logging output |
| logpath | File path to place log files | $HOME/.cache/tv_viewer/ | |
| networkcheckonoff | or or off | on | toggles network test  uses ping |
| networkurl | url | www.tvmaze.com | url to test by network test  |

## Dependencies

| Dependencies | Usage |  URL |
| ------ | ------ | ----- |
| prettytable 3.3.0 | Used to format Data into tables | [ Link ](https://github.com/jazzband/prettytable) |
| pytvmaze 2.0.8 | Python interface to TV Maze API | [link](https://github.com/srob650/pytvmaze) |
| pyqt5 5.15.6 | GUI toolkit | [Link](http://pyqt.sourceforge.net/Docs/PyQt5/) |


## Features

From the menu bar a user can select about and exit options.
From here they can also view latest log file and configuration file contents.
The TV maze API associates a unique ID with each TV show called the Maze_ID.
On the main screen the user is prompted to enter name of show in input box.
The software then returns a list of television shows based on the input.
The user can then select the show by row number and is presented with 
various details of it. From here they select more detailed information 
by selecting one of the radio buttons and pressing details.
Options include overview, seasons, cast, 
crew, episodes and more miscellaneous information. 
They can also view and/or toggle the favourite status of  show by 
pressing delete or add favourite button. 

The software also includes a favourite function where user 
can store favourites TV shows in a database.
The database has one table show and two fields name and number.
the maze_ID of the show is stored at number.
The contents of the database can be displayed by pressing Favourites  button.
Favourites records can be added by entering a maze_id in input box 
and pressing add favourite button, records can be deleted by adding a maze_id 
of show in database and pressing delete favourite button.
The favourite section will also show next episode date 
and days till next episode. You also access the tv show details screen from here 
by adding a maze_id and pressing search.
A reset and exit button is also available. 
There is a status light with 3 colours

1. Green : ready 
2. Yellow : busy , accessing network or files
3. Red : network check failed, The network check is carried out at start up and when certain buttons fail it can turned off.

## Screenshot


There are screenshots in this repository in documentation folder. 

![ image ](https://github.com/gavinlyonsrepo/tv_viewer/blob/master/Documentation/screenshots/tv_show_info_screen.png)
