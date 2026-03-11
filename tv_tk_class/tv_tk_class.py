#!/usr/bin/env python3
"""
filename:    tv_tk_class.py 
Description: module called by tv_viewer
    contains a class to handle the Tkinter GUI of program
"""
# ========================= IMPORTS ====================
import subprocess
import textwrap
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, font as tkfont

# my modules
from tv_api_work import tv_api_work as myApi
from tv_sqllite import tv_sqllite as mySql
from tv_logger_conf import tv_logger_conf as myLog

# ================== GLOBALS ==========================
LOGGER = myLog.my_logging(__name__)
my_tv_api = myApi.TvApi("myapiobject")
my_tv_sql = mySql.TvSqLight("mysqlobject")

# ================== CLASSES SECTION ===============

class UiMainWindow(): # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """Main window class for the tv_viewer Tkinter GUI"""

    def __init__(self, root):
        self.root = root
        self.screen_status_dict = {
            "mainScreen": 0, "selectShowScreen": 1,
            "favScreen": 2, "showDetailsScreen": 3}
        self.screen_status = self.screen_status_dict["mainScreen"]
        self.radio_var = tk.IntVar(value=1)
        self._status_after_id = None
        self.overview_rbtn = None
        self.actors_rbtn = None
        self.seasons_rbtn = None
        self.crews_rbtn = None
        self.info_rbtn = None
        self.episode_rbtn = None
        self._setup_ui()
        self._connect_callbacks()
        my_tv_sql.create_db()
        self.network_check()
        self.start_screen()

    # =================== UI CONSTRUCTION ===================

    def _setup_ui(self):  # pylint: disable=too-many-locals, too-many-statements
        """Build all widgets and lay them out with grid"""
        self.root.title("Tv Viewer")
        resolution = myLog.settings.getstr("Display", "screen_resolution", fallback=str("1100x800"))
        font_size =  myLog.settings.getint("Display", "font_size", fallback=int(11))
        font_name =  myLog.settings.getstr("Display", "font_name", fallback=str("TkFixedFont"))
        self.root.geometry(resolution)
        self.root.resizable(True, True)

        # Root expands to fill window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # Main container frame
        mf = tk.Frame(self.root)
        mf.grid(row=0, column=0, sticky="nsew")
        self.main_frame = mf
        # Columns 0-7 share the listbox area; column 8 is the right panel
        for c in range(8):
            mf.columnconfigure(c, weight=1)
        mf.columnconfigure(8, weight=0)
        # Row 1 (listbox) expands vertically
        mf.rowconfigure(1, weight=1)
        # --- Menu bar ---
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menu_file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Menu", menu=self.menu_file)
        # --- Screen title label ---
        self.mainlbl = tk.Label(mf, text="Information Display",
                                relief=tk.SUNKEN, anchor="w")
        self.mainlbl.grid(row=0, column=0, columnspan=8,
                          sticky="ew", padx=5, pady=5)
        # --- Busy/status indicator (coloured box, top-right)
        self.busy_btn = tk.Label(mf, text="Status", bg="green", width=12, relief=tk.RAISED)
        self.busy_btn.grid(row=2, column=8, sticky="w", padx=5, pady=5)
        # --- Listbox with vertical scrollbar ---
        list_frame = tk.Frame(mf, relief=tk.SUNKEN, bd=2)
        list_frame.grid(row=1, column=0, columnspan=8,
                        sticky="nsew", padx=5, pady=2)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        mono = tkfont.Font(family=font_name, size=font_size)
        self.listinfo = tk.Listbox(list_frame, font=mono,
                                   selectmode=tk.SINGLE,
                                   activestyle="none")
        vscroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL,
                               command=self.listinfo.yview)
        hscroll = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL,
                       command=self.listinfo.xview)
        self.listinfo.config(yscrollcommand=vscroll.set,
                     xscrollcommand=hscroll.set)
        self.listinfo.grid(row=0, column=0, sticky="nsew")
        vscroll.grid(row=0, column=1, sticky="ns")
        hscroll.grid(row=1, column=0, sticky="ew")
        # --- Radio buttons (right panel) ---
        radio_frame = tk.Frame(mf)
        radio_frame.grid(row=1, column=8, sticky="n", padx=10, pady=5)
        radio_opts = [
            ("Overview",  1, "overview_rbtn"),
            ("Actors",    2, "actors_rbtn"),
            ("Seasons",   3, "seasons_rbtn"),
            ("Crews",     4, "crews_rbtn"),
            ("More Info", 5, "info_rbtn"),
            ("Episodes",  6, "episode_rbtn"),
        ]
        for i, (label, val, attr) in enumerate(radio_opts):
            btn = tk.Radiobutton(radio_frame, text=label,
                                 variable=self.radio_var, value=val,
                                 state=tk.DISABLED)
            btn.grid(row=i, column=0, sticky="w", pady=8)
            setattr(self, attr, btn)
        # --- Entry Box and Label sub frame---
        input_frame = tk.Frame(mf)
        input_frame.grid(row=2, column=0, columnspan=8, sticky="ew", padx=5, pady=2)
        self.txtlbl = tk.Label(input_frame, text="Input Box", relief=tk.SUNKEN)
        self.txtlbl.pack(side=tk.LEFT)
        self.text_enter = tk.Entry(input_frame, width=50)
        self.text_enter.pack(side=tk.LEFT, padx=5)
        # --- Button row ---
        btn_frame = tk.Frame(mf)
        btn_frame.grid(row=3, column=0, columnspan=9,
                       sticky="ew", padx=5, pady=5)
        s = {"relief": tk.GROOVE, "bd": 3, "width": 12}
        self.search_btn     = tk.Button(btn_frame, text="Search",       **s)
        self.detail_btn     = tk.Button(btn_frame, text="Details",      state=tk.DISABLED, **s)
        self.scale          = tk.Scale(btn_frame, bd=3, from_=1, to=6,
                                       orient=tk.HORIZONTAL, length=80,
                                       showvalue=False, bg="black")
        self.fav_btn        = tk.Button(btn_frame, text="Favorites",    **s)
        self.add_fav_btn    = tk.Button(btn_frame, text="Add Favorite", state=tk.DISABLED, **s)
        self.remove_fav_btn = tk.Button(btn_frame, text="Del Favorite", state=tk.DISABLED, **s)
        self.reset_btn      = tk.Button(btn_frame, text="Reset",        **s)
        self.exit_btn       = tk.Button(btn_frame, text="Exit",         **s)
        for widget in (self.search_btn, self.detail_btn, self.scale,
                       self.fav_btn, self.add_fav_btn, self.remove_fav_btn,
                       self.reset_btn, self.exit_btn):
            widget.pack(side=tk.LEFT, padx=3)
        # --- Status bar (bottom) ---
        self.statusbar = tk.Label(mf, text="", relief=tk.SUNKEN, anchor="w")
        self.statusbar.grid(row=4, column=0, columnspan=9,
                            sticky="ew", padx=5, pady=2)

    def _connect_callbacks(self):
        """Wire up all button commands, menu items, and key bindings"""
        self.search_btn.config(command=self.search_button_click)
        self.detail_btn.config(command=self.details_button_click)
        self.scale.config(command=self.scale_changed)
        self.fav_btn.config(command=self.fav_button_click)
        self.add_fav_btn.config(command=self.addfav_button_click)
        self.remove_fav_btn.config(command=self.delfav_button_click)
        self.reset_btn.config(command=self.reset_screen)
        self.exit_btn.config(command=self.close_application)

        self.listinfo.bind("<<ListboxSelect>>", self.selection_changed)

        self.menu_file.add_command(label="About",      accelerator="Ctrl+A",
                                   command=self.display_about)
        self.menu_file.add_command(label="Log File",    accelerator="Ctrl+L",
                                   command=self.log_file_view)
        self.menu_file.add_command(label="Config File", accelerator="Ctrl+G",
                                   command=self.config_file_view)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Desktop Entry", accelerator="Ctrl+D",
                                   command=self.desktop_entry)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit",       accelerator="Ctrl+Q",
                                   command=self.close_application)

        self.root.bind("<Control-a>", lambda e: self.display_about())
        self.root.bind("<Control-l>", lambda e: self.log_file_view())
        self.root.bind("<Control-g>", lambda e: self.config_file_view())
        self.root.bind("<Control-d>", lambda e: self.desktop_entry())
        self.root.bind("<Control-q>", lambda e: self.close_application())

    # =================== LISTBOX / ENTRY HELPERS ===================

    def _listinfo_add(self, text):
        """Insert text into listbox, splitting on newlines so each line is its own item"""
        for line in str(text).split('\n'):
            self.listinfo.insert(tk.END, line)

    def _listinfo_clear(self):
        self.listinfo.delete(0, tk.END)

    def _entry_get(self):
        return self.text_enter.get()

    def _entry_set(self, text):
        self.text_enter.delete(0, tk.END)
        self.text_enter.insert(0, str(text))

    def _entry_clear(self):
        self.text_enter.delete(0, tk.END)

    # =================== STATUS BAR ===================

    def show_status(self, text, duration=0):
        """Display a message in the status bar; auto-clear after duration ms if given"""
        self.statusbar.config(text=text)
        if self._status_after_id:
            self.root.after_cancel(self._status_after_id)
            self._status_after_id = None
        if duration:
            self._status_after_id = self.root.after(
                duration, lambda: self.statusbar.config(text=""))

    # =================== CORE METHODS ===================

    def close_application(self):
        """Exit button / Ctrl+Q — close DB and destroy window"""
        my_tv_sql.close_db()
        LOGGER.info(' Program Exiting ')
        self.root.destroy()

    def scale_changed(self, value):
        """Scale moved — select the matching radio button"""
        self.radio_var.set(int(value))

    def busy_indicator(self, status):
        """Toggle the coloured status box green/yellow/red"""
        colours = {"ready": "green", "busy": "yellow", "error": "red"}
        self.busy_btn.config(bg=colours.get(status, "green"))
        if status == "busy":
            self.root.update()  # force immediate repaint

    def network_check(self):
        """Ping the configured URL; colour the status box accordingly"""
        try:
            network_url = myLog.settings.getstr("Network",
                                                "mazetv_url", fallback=str("www.tvmaze.com"))
            network_on_off = myLog.settings.getbool("Network",
                                                    "networkOnOff", fallback=1)
            debug_on = myLog.settings.getbool("Debug", "debugOnOff", fallback=0)
            if network_on_off == 1:
                if debug_on == 1:
                    result = subprocess.call(
                        ['ping', '-q', '-c', '1', network_url])
                else:
                    # silent ping
                    result = subprocess.call(
                        ['ping', '-c', '1', network_url],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                if result == 0:
                    self.busy_btn.config(bg="green")
                    LOGGER.info("network OK :: %s", network_url)
                elif result == 2:
                    self.busy_indicator("error")
                    LOGGER.exception(" Problem with network no response :: %s", network_url)
                else:
                    self.busy_indicator("error")
                    LOGGER.exception(" Problem with network failed ping :: %s", network_url)
        except Exception as error: # pylint: disable=(broad-exception-caught)
            LOGGER.exception("Problem with network %s", error)
            self.busy_indicator("error")

    def set_radio_buttons(self, on_off):
        """Enable or disable all radio buttons. Clears selection when disabling."""
        state = tk.NORMAL if on_off else tk.DISABLED
        for btn in (self.overview_rbtn, self.actors_rbtn, self.seasons_rbtn,
                    self.crews_rbtn, self.info_rbtn, self.episode_rbtn):
            btn.config(state=state)
        if not on_off:
            self.radio_var.set(1)

    def reset_screen(self):
        """Reset button — return everything to the initial state"""
        self.screen_status = self.screen_status_dict["mainScreen"]
        self._listinfo_clear()
        self._entry_clear()
        self.mainlbl.config(text="Information Display")
        self.search_btn.config(state=tk.NORMAL)
        self.detail_btn.config(state=tk.DISABLED)
        self.fav_btn.config(state=tk.NORMAL)
        self.add_fav_btn.config(state=tk.DISABLED)
        self.remove_fav_btn.config(state=tk.DISABLED)
        self.set_radio_buttons(False)
        self.scale.set(1)
        self.busy_btn.config(bg="green")
        self.network_check()
        self.start_screen()

    def start_screen(self):
        """Populate listbox with the welcome/help text"""
        self._listinfo_add(" Welcome:")
        self._listinfo_add("\n Press Search button to search for TV Series")
        self._listinfo_add("\n based on text in Input box")
        self._listinfo_add("\n Press View Favs button for Favourites screen")
        self._listinfo_add("\n Press Reset button to reset screen")

    # =================== MENU ACTIONS ===================

    def desktop_entry(self):
        """ Handles press of desktop entry from menu"""
        self._listinfo_clear()
        self.busy_indicator("busy")
        success, messages = myLog.install_desktop_entry()
        for line in messages:
            self._listinfo_add(line)
        if success:
            self.show_status("Desktop Entry install ran without Error", 2000)
        else:
            self.show_status("Desktop Entry install failed", 2000)
        self.busy_indicator("ready")

    def display_about(self):
        """ Handles press of about from menu """
        self._listinfo_clear()
        self._listinfo_add(
            f"\n GUI program to view tv program details using tvmaze API"
            f"\n Version :: 3.0.3"
            f"\n Copyright :: Gavin Lyons 2017 GPL"
            f"\n URL :: https://github.com/gavinlyonsrepo/tv_viewer"
        )

    def log_file_view(self):
        """ Handles press of view log file from menu"""
        self._listinfo_clear()
        try:
            log_file_path = myLog.settings.getstr("Logging", "logging_dir", fallback=str("/tmp/"))
            log_file_dir = Path(log_file_path)
            newest = max(log_file_dir.glob('TV*.log'), key=lambda f: f.stat().st_ctime)
            self._listinfo_add("Newest log file contents below :: " + str(newest))
            with open(newest, "r", encoding="utf-8") as fh:
                self._listinfo_add(fh.read())
        except ValueError:
            self._listinfo_add("No log files found at :: " + str(log_file_path))
            LOGGER.exception(" No log files found ")
        except FileNotFoundError:
            self.show_status("Problem reading newest log file :: FileNotFoundError", 2000)
            LOGGER.exception("Error reading log files FileNotFoundError")
        except PermissionError as error:
            self.show_status("Problem reading newest log file :: PermissionError", 2000)
            LOGGER.exception(" Error reading log files %s ", error)
        except OSError as error:
            self.show_status("Problem reading newest log file", 2000)
            LOGGER.exception(" Error reading log files %s ", error)

    def config_file_view(self):
        """ Handles press of view config file from menu"""
        self._listinfo_clear()
        try:
            config_file_path = myLog.Settings.CONFIG_PATH
            self._listinfo_add("Contents of config file at :: " + str(config_file_path))
            with open(config_file_path, "r", encoding="utf-8") as fh:
                self._listinfo_add(fh.read())
        except FileNotFoundError:
            self.show_status("Problem reading config file :: FileNotFoundError", 2000)
            LOGGER.exception("Error reading config files FileNotFoundError")

    # =================== BUTTON HANDLERS ===================

    def search_button_click(self):
        """Search button dispatcher — behaviour depends on current screen"""
        self.fav_btn.config(state=tk.DISABLED)
        if self.screen_status == 0:
            self.search_button_zero()
        elif self.screen_status == 1:
            self.search_button_one()
        elif self.screen_status == 2:
            self.search_button_two()

    def search_button_zero(self):
        """Search from main screen — look up a show by name"""
        if self._entry_get():
            self.network_check()
            self.busy_indicator("busy")
            items = my_tv_api.search_tv_series(self._entry_get())
            self.busy_indicator("ready")
            if not items:
                messagebox.showwarning(
                    "Message Box 1014",
                    "There Is No Matching Tv Show :- " + self._entry_get())
                self.fav_btn.config(state=tk.NORMAL)
            else:
                self._listinfo_clear()
                for line in str(items).split('\n'):
                    self.listinfo.insert(tk.END, line)
                self._entry_clear()
                self.screen_status = self.screen_status_dict["selectShowScreen"]
                self.mainlbl.config(text="TV show selection screen")
        else:
            messagebox.showwarning(
                "Message Box 1012",
                "Enter a TV show name in Input Box & press Enter")
            self.fav_btn.config(state=tk.NORMAL)

    def search_button_one(self):
        """Search/select from show-list screen"""
        items = None
        try:
            # Part 1 — empty input box?
            if not self._entry_get():
                self.show_status("Select a Row number and press Enter", 2000)
                return
            self.busy_indicator("busy")
            # Part 2 — fetch show data
            if not self._entry_get().isdecimal():
                self.show_status(
                    "Not a Valid row Number :: " + self._entry_get(), 2000)
                self.busy_indicator("ready")
                self._entry_clear()
                return
            items = my_tv_api.show_tv_series(self._entry_get(), "No show name")
            # Part 3 — did the API return anything?
            if not items:
                messagebox.showwarning(
                    "Message Box 1011",
                    "Invalid Data from API for this show:: " + str(items))
            else:
                # Part 4 — display
                self.screen_status = self.screen_status_dict["showDetailsScreen"]
                self._listinfo_clear()
                for line in str(items).split('\n'):
                    self.listinfo.insert(tk.END, line)
                self.search_btn.config(state=tk.DISABLED)
                self.detail_btn.config(state=tk.NORMAL)
                self.remove_fav_btn.config(state=tk.NORMAL)
                self.add_fav_btn.config(state=tk.NORMAL)
                self.set_radio_buttons(True)
                self.mainlbl.config(text="Tv show information screen")
                # Part 5 — extract maze_id from first data row and put in input box
                maze_id = items.get_string(
                    header=False,
                    start=0, end=1,
                    fields=["Value"]).strip()
                if maze_id:
                    self._entry_set(maze_id)
        except ValueError as error:
            LOGGER.exception("Invalid value in show search %s", error)
            self.show_status("Invalid data :: " + str(error), 2000)
        except AttributeError as error:
            LOGGER.exception("Unexpected None from API %s", error)
            self.show_status("No data returned from API", 2000)
        finally:
            self.busy_indicator("ready")


    def search_button_two(self):
        """Search/select from favs screen """
        items = None
        try:
            # Part 1 — empty input box?
            if not self._entry_get():
                self.show_status("Pick a Fav show and press Enter", 2000)
                return
            self.busy_indicator("busy")
            # Part 2 — fetch show data  # maze ID from favourites
            maze_id = str(int(self._entry_get()))   # strip any leading zeros
            showflag = my_tv_sql.scan_db(maze_id)
            if not showflag:
                self._entry_clear()
                self.show_status("Not a Valid maze ID", 2000)
                self.busy_indicator("ready")
                return
            show_name = my_tv_api.showname_get(maze_id)
            items = my_tv_api.show_tv_series(0, str(show_name))
            self.busy_indicator("ready")
            # Part 3 — did the API return anything?
            if not items:
                messagebox.showwarning(
                    "Message Box 1011",
                    "Invalid Data from API for this show:: " + str(items))
            else:
                # Part 4 — display
                self.screen_status = self.screen_status_dict["showDetailsScreen"]
                self._listinfo_clear()
                for line in str(items).split('\n'):
                    self.listinfo.insert(tk.END, line)
                self.search_btn.config(state=tk.DISABLED)
                self.detail_btn.config(state=tk.NORMAL)
                self.remove_fav_btn.config(state=tk.NORMAL)
                self.add_fav_btn.config(state=tk.NORMAL)
                self.set_radio_buttons(True)
                self.mainlbl.config(text="Tv show information screen")
        except ValueError as error:
            LOGGER.exception("Invalid value in show search %s", error)
            self.show_status("Invalid data :: " + str(error), 2000)
        except AttributeError as error:
            LOGGER.exception("Unexpected None from API %s", error)
            self.show_status("No data returned from API", 2000)
        finally:
            self.busy_indicator("ready")

    def details_button_click(self):
        """Details button — show whichever radio button option is selected"""
        self.busy_indicator("busy")
        self._entry_clear()
        self._listinfo_clear()
        self.remove_fav_btn.config(state=tk.DISABLED)
        self.add_fav_btn.config(state=tk.DISABLED)
        rv = self.radio_var.get()
        if rv == 1:
            overview_text = str(my_tv_api.overview(1))
            for line in textwrap.wrap(overview_text, width=50):
                self.listinfo.insert(tk.END, line)
        elif rv == 2:
            self._listinfo_add(str(my_tv_api.actors(0)))
        elif rv == 3:
            self._listinfo_add(str(my_tv_api.seasons(0)))
        elif rv == 4:
            self._listinfo_add(str(my_tv_api.crews(0)))
        elif rv == 5:
            self._listinfo_add(str(my_tv_api.more_info(1)))
        elif rv == 6:
            self._listinfo_add(str(my_tv_api.episode(0)))
        else:
            self._listinfo_add("Select an option from side bar:-")
        self.busy_indicator("ready")

    def fav_button_click(self):
        """Favourites button — load and display the favourites database"""
        self.network_check()
        self.remove_fav_btn.config(state=tk.NORMAL)
        self.add_fav_btn.config(state=tk.NORMAL)
        self.fav_btn.config(state=tk.DISABLED)
        self.search_btn.config(state=tk.NORMAL)
        self.screen_status = self.screen_status_dict["mainScreen"]
        self._listinfo_clear()
        self.busy_indicator("busy")
        try:
            items = my_tv_api.favour_show(my_tv_sql.display_db())
            if items:
                for line in str(items).split('\n'):
                    self.listinfo.insert(tk.END, line)
            else:
                self.listinfo.insert(tk.END, "No Favourites in database")
        except TypeError as error:
            LOGGER.exception("Problem loading Favourites menu %s", error)
            self.show_status("Error loading favourites", 2000)
        except tk.TclError as error:
            LOGGER.exception("UI error loading Favourites menu %s", error)
            self.show_status("UI error loading favourites", 2000)
        else:
            self.mainlbl.config(text="Favourites Information Screen")
            self.screen_status = self.screen_status_dict["favScreen"]
            self.show_status("Favourites Information Screen", 2000)
        finally:
            self.busy_indicator("ready")

    def addfav_button_click(self):
        """Add Favourite button — validate maze ID and insert into database"""
        try:
            self.detail_btn.config(state=tk.DISABLED)
            self.set_radio_buttons(False)
            mazeid = str(int(self._entry_get()))    # strips leading zeros
            if mazeid:
                self.busy_indicator("busy")
                in_database = my_tv_sql.scan_db(mazeid)
                if in_database:
                    messagebox.showinfo(
                        "Message Box 1004",
                        "That maze_id already in the database:- " + mazeid)
                else:
                    show_name = my_tv_api.showname_get(mazeid)
                    if show_name != "Error":
                        my_tv_sql.add_db(mazeid, show_name)
                        self.fav_button_click()
                        messagebox.showinfo(
                            "Message Box 1005",
                            "Added maze_id to the database:- " + mazeid)
                    else:
                        messagebox.showwarning(
                            "Message Box 1006",
                            "Cannot find that Maze_ID with API :- ")
                self.busy_indicator("ready")
            else:
                messagebox.showwarning(
                    "Message Box 1007",
                    "Add a Maze_Id to input box and press again :-")
        except ValueError as error:
            LOGGER.exception(" Invalid maze ID entered :: %s", error)
            self.show_status("Invalid Maze ID — numbers only", 2000)

    def delfav_button_click(self):
        """Del Favourite button — validate maze ID and remove from database"""
        try:
            self.detail_btn.config(state=tk.DISABLED)
            self.set_radio_buttons(False)
            mazeid = str(int(self._entry_get()))    # strips leading zeros
            if mazeid:
                self.busy_indicator("busy")
                in_database = my_tv_sql.scan_db(mazeid)
                if in_database:
                    my_tv_sql.del_db(mazeid)
                    self.fav_button_click()
                    messagebox.showinfo(
                        "Message Box 1000",
                        "Removed maze_id from the database:- " + mazeid)
                else:
                    messagebox.showinfo(
                        "Message Box 1002",
                        "maze_id is not in the Favorite database:- " + mazeid)
                self.busy_indicator("ready")
            else:
                messagebox.showwarning(
                    "Message Box 1003",
                    "Add a valid Maze_Id to input box and press again :- ")
        except ValueError as error:
            LOGGER.exception(" Failure in delfav_button_click method :: %s", error)
            self.show_status("Invalid Maze ID — numbers only", 2000)

    def selection_changed(self, _ ):
        """Listbox selection changed — populate the input box with the relevant value"""
        try:
            selection = self.listinfo.curselection()
            if not selection:
                return
            index = selection[0]
            line = self.listinfo.get(index)
            if self.screen_status == self.screen_status_dict["favScreen"]:
                if index > 2:   # skip top border, header, middle border
                    self._entry_set(line.split()[2])    # column index 2 = Maze_id
                else:
                    self._entry_set(" ")
            elif self.screen_status == self.screen_status_dict["selectShowScreen"]:
                if index > 2:   # skip top border, header, middle border
                    self._entry_set(line.split()[0])
                else:
                    self._entry_set("0")
        except IndexError as error:
            self._entry_set(" ")
            LOGGER.exception(" Failure in selection_changed :: %s", error)


# =====================MAIN====================
def test(text):
    """ Test module imported function """
    LOGGER.info(text)


if __name__ == '__main__':
    test("main")
else:
    test(" Imported " + __name__)
# =====================END==========
