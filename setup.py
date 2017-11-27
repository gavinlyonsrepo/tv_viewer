from setuptools import setup

setup(
    name="tv_viewer",
    version="1.0.2",
    author="Gavin Lyons",
    author_email="glyons66@hotmail.com",
    description="Python PyQt5 GUI to view tv program details using tvmaze API and SQLite",
    license="GPL",
    keywords="televison tv_viewer tv maze SQLite PyQt gavin lyons schedule",
    url="https://github.com/gavinlyonsrepo/tv_viewer",
    download_url='https://github.com/gavinlyonsrepo/tv_viewer/archive/1.0.tar.gz',
    packages=['tv_viewer','tv_qt_class','tv_sqllite','tv_api_work'],
    data_files=[('/usr/share/doc/tv_viewer/', ['README.md']),
                 ('/usr/share/pixmaps/', ['desktop/tv_viewer.png']),
                 ('/usr/share/applications/', ['desktop/tv_viewer.desktop'])],
    install_requires=['pip','pytvmaze','prettytable',],
    setup_requires=['pip'],
    scripts=['tv_viewer/tv_viewer.py'],
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
