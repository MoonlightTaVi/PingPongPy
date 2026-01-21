"""
This module contains tools that can be used to help 
the use operating with the web browser 
(open a page, copy some text to clipboard, etc.).
"""
__version__ = "1.0.0"
__author__ = "MoonlightTaVi"


from configparser import ConfigParser
import tkinter as tk
import webbrowser


class BrowserPage:
    """
    A small util that can open a browser page 
    and copy some text to clipboard.
    Opens the router page, buffering the user credentials to it,
    by default (on the start() call.)
    """
    def __init__(self) -> None:
        self.COPY_TEXT: str = "admin"
        self.URL: str = "http://192.168.0.1/"
        self.BUFFER_LIFETIME: int = 300
    def copy_to_clipboad(self, copied_text: str):
        """Copy the specified text to clipboard"""
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(copied_text)
        root.update()
        root.after(self.BUFFER_LIFETIME, root.destroy)
        root.mainloop()
    def open_browser(self, url: str):
        """Open URL in the default browser"""
        webbrowser.open(url)
    def start(self):
        """Copy the router password and open in browser."""
        self.copy_to_clipboad(self.COPY_TEXT)
        self.open_browser(self.URL)
    def load_config(self, config: ConfigParser):
        """Loads the settings preset from a config."""
        self.COPY_TEXT = config["API"]["password"]
        self.URL = config["API"]["URL"]
        self.BUFFER_LIFETIME = config.getint("OTHER","buffer_delay")