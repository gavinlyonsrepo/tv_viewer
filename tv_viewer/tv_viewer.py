#!/usr/bin/env python3
""" 
filename: tv_viewer 
desc: GUI to view tv program details using TV maze application
programming interface. Written in python 3 and Tkinter,
it also stores user favourites in an SQLite database.
This file is main script and entry point"""

# ==========================IMPORTS======================
import sys
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path
# My modules
from tv_tk_class import tv_tk_class as myTkGUI
from tv_logger_conf import tv_logger_conf as my_log

__version__ = "3.0.0"

# =====================MAIN===============================
if __name__ == "__main__":
    #  logger
    logger = my_log.my_logging(__name__)
    logger.info("  Main Loop Start")
    # Configure TK root window
    root = tk.Tk()
    ICON_REF = None  # prevent GC of icon image
    # set global font size
    font_size = my_log.settings.getint("Display", "font_size", fallback=int(11))
    for name in tkfont.names(root):
        f = tkfont.nametofont(name)
        f.config(size=font_size)
    # set Icon
    if sys.platform.startswith("linux"):
        icon_path = Path.home() / ".local/share/icons/tv_viewer.png"
        if icon_path.exists():
            try:
                ICON_REF = tk.PhotoImage(file=str(icon_path))
                root.iconphoto(True, ICON_REF )
            except tk.TclError as e:
                logger.warning("Could not set window icon: %s", e)
            except OSError as e:
                logger.warning("Could not read icon file: %s", e)
    # Run the main loop
    ui = myTkGUI.UiMainWindow(root)
    root.mainloop()
