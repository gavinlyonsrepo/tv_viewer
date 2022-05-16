from setuptools import setup
from sys import platform
import os
        
 
setup(
    name="tv_viewer",
    version="2.2",
    author="Gavin Lyons",
    author_email="glyons66@hotmail.com",
    description="Python PyQt5 GUI to view tv program details using tvmaze API and SQLite",
    license="GPL",
    keywords="televison tv_viewer tv maze SQLite PyQt gavin lyons schedule API GUI",
    url="https://github.com/gavinlyonsrepo/tv_viewer",
    download_url='https://github.com/gavinlyonsrepo/tv_viewer/archive/2.2.tar.gz',
    packages=['tv_viewer','tv_qt_class','tv_sqllite','tv_api_work','tv_logger_conf'],
    install_requires=['pip','pytvmaze','prettytable',],
    setup_requires=['pip'],
    scripts=['tv_viewer/tv_viewer.py'],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
