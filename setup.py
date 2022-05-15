from setuptools import setup
from sys import platform

if platform == 'win32':
    setup(
        name="tv_viewer",
        version="2.0",
        author="Gavin Lyons",
        author_email="glyons66@hotmail.com",
        description="Python PyQt5 GUI to view tv program details using tvmaze API and SQLite",
        license="GPL",
        keywords="televison tv_viewer tv maze SQLite PyQt gavin lyons schedule API GUI",
        url="https://github.com/gavinlyonsrepo/tv_viewer",
        download_url='https://github.com/gavinlyonsrepo/tv_viewer/archive/2.0.tar.gz',
        packages=['tv_viewer','tv_qt_class','tv_sqllite','tv_api_work','tv_logger_conf'],
        install_requires=['pip','pytvmaze','prettytable',],
        setup_requires=['pip'],
        scripts=['tv_viewer/tv_viewer.py'],
        classifiers=[
            "Programming Language :: Python :: 3.10.4",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
        )
else:
    setup(
        name="tv_viewer",
        version="2.0",
        author="Gavin Lyons",
        author_email="glyons66@hotmail.com",
        description="Python PyQt5 GUI to view tv program details using tvmaze API and SQLite",
        license="GPL",
        keywords="televison tv_viewer tv maze SQLite PyQt gavin lyons schedule API GUI",
        url="https://github.com/gavinlyonsrepo/tv_viewer",
        download_url='https://github.com/gavinlyonsrepo/tv_viewer/archive/2.0.tar.gz',
        packages=['tv_viewer','tv_qt_class','tv_sqllite','tv_api_work','tv_logger_conf'],
        data_files=[('/usr/share/doc/tv_viewer/', ['README.md']),
                     ('/usr/share/pixmaps/', ['desktop/tv_viewer.png']),
                     ('/usr/share/applications/', ['desktop/tv_viewer.desktop'])],
        install_requires=['pip','pytvmaze','prettytable',],
        setup_requires=['pip'],
        scripts=['tv_viewer/tv_viewer.py'],
        classifiers=[
            "Programming Language :: Python :: 3.10.4",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ], 
        )
