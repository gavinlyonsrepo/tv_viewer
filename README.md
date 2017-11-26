
Overview
--------------------------------------------
* Name: tv_viewer
* Title : Graphical user interface to view tv show details using TV maze API 
* Description: GUI to view tv program details using TV maze application 
programming interface. Written in python 3 and PyQt 5, it also stores 
user favourites in an SQLite database. 
It uses python module pytvmaze to interface with API 
and python module prettytable to help display results.
* Author: Gavin Lyons 

Table of contents
---------------------------

  * [Overview](#overview)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Files and setup](#files-and-setup)
  * [Dependencies](#dependencies)
  * [Features](#features)
  * [To Do](#to-do)
  * [See Also](#see-also)
  * [Communication](#communication)
  * [History](#history)
  * [Copyright](#copyright)

Installation
-----------------------------------------------

If you are an Arch linux OS user 
tv_viewer can be installed by PKGBUILD. The PKGBUILD file is available in the AUR - Arch user repository. 

    AUR package name :tv_viewer
    AUR maintainer : glyons
    AUR location: https://aur.archlinux.org/packages/tv_viewer/


For other Linux OS users.
Make sure that python 3 and pip3 have been installed on your machine, then: 
```sh
sudo pip3 install tv_viewer
```

I have not tested it in windows 10 
for this initial release version see to do list.

Usage
-------------------------------------------
type in terminal to launch or select from Desktop under Multimedia

```sh
tv_viewer.py 
```

Files and setup
-----------------------------------------

| File Path | Description |
| ------ | ------ |
| $HOME/.config/tv_viewer/fav.db | Database created by program |
| /usr/share/doc/tv_viewer/README.md | Help |
| /usr/share/pixmaps/tv_viewer.png | icon |
| tv_viewer.py | main executable python script |
| tv_qt_class.py | python module dealing with PyQt code |
| tv_sqllite.py | python module dealing with SQLite code |
| tv_api_work.py | python module dealing with Pytvmaze code |


Dependencies
-------------------------------------
| Dependencies| Usage |
| ------ | ------ |
| prettytable (0.7.2) | used to format text extracted from API into tables |
| pytvmaze (2.0.8) | Python interface to TV Maze API |
| pyqt5 (5.9.2) | GUI tool |

Features
----------------------
From the menu bar a user can select about, help and exit options.


On the main screen the user is prompted to enter name of show in input box.
The software then returns a list of television shows based on the input.
The user can then select the show by row number and is presented with 
various details of it. From here they select more detailed information 
by selecting one of the radio buttons and pressing *Select*. 
Options include overview, seasons, cast, 
crew, episodes and more miscellaneous information. 


The software also includes a favourite function where user 
can store favourites TV shows in a database.
The database has one table *shows* and two fields *name* and *number*.
the maze_ID of the show is stored at number.
The contains of database can be displayed by pressing *View Favs* button.
Favourites records can be added by entering an existing maze_id in input box 
and pressing *Edit Favs* button, records can be deleted by adding a maze_id 
of show not in database and pressing *Edit Favs* button.
The favourite section will also show next episode date 
and days till next episode.


A reset and exit button is also available. 

Exceptions are generated by software as a result of missing and incomplete 
API data by TV maze for some shows. These are caught and outputted 
to terminal, In future versions these will be logged. 

To Do
-------------------------------------
* Ability to access favourites database from show TV details screens.
* Ability to access full show TV details from favourites screen.
* Code the "Upcoming shows" Function.
* Logging and enhanced error handling.
* Optimise text formatting in favourites screen.
* Test installation in windows environment.


See Also
-----------
* [TV maze API](http://www.tvmaze.com/api)
* [pytvmaze Python interface to TV Maze API ](https://github.com/srob650/pytvmaze)
* [prettytable python module](https://github.com/dprince/python-prettytable)
* [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/)
* [SQLite](https://sqlite.org/)


Communication
-----------
If you should find a bug or you have any other query, 
please send a report.
Pull requests, suggestions for improvements
and new features welcome.
* Contact: Upstream repo at github site below or glyons66@hotmail.com
* Upstream repository: https://github.com/gavinlyonsrepo/tv_viewer

History
------------------

See changelog.md in documentation section for version control history


Copyright
---------
Copyright (C) 2017 Gavin Lyons 
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public license published by
the Free Software Foundation, see LICENSE.md in documentation section 
for more details
