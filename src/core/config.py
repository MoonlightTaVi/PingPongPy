"""
Utilities for configuration file reading.
"""
__version__ = "1.1.2"
__author__ = "MoonlightTaVi"


from configparser import ConfigParser


class ConfigReader:
    """A simple util to read INI configuration from a CONFIG.INI file."""

    def __init__(self, data_folder: str = "data") -> None:
        """
        Reads a CONFIG.INI file that is placed into the specified directory;
        stores the obtained ConfigParser object as its state field.
        """
        self.config = ConfigParser()
        self.config.read(f"{data_folder}/CONFIG.INI")

    def get_config(self) -> ConfigParser:
        """Returns the pre-loaded config object."""
        return self.config


class AppConfig:
    """Data object that manages the configuration of the application."""

    def __init__(self) -> None:
        """Initializes the default configuration."""
        self.SLEEP_TIME: float = 5
        self.FAIL_SLEEP_TIME: float = 5
        self.ASCII_FILE: str = "ascii_fu.txt"
        self.UPDATE_TIME: float = 20
        self.ASCII_ENABLED: bool = True
        self.MAX_FAILS: int = 5
        self.DISCONNECT_THRESHOLD = 15
        self.OPEN_BROWSER: bool = True
        self.REBOOT: bool = False
        self.PING_URL: str = "google.com"
        # Fallback is performed when the connection is completely lost
        #  0 - Do nothing
        #  1 - Pause and ask the user whether to reboot manually again
        #  2 - Try to reboot automatically yet a couple of times, then pause
        self.FALLBACK_MODE: int = 0

    def load_config(self, config: ConfigParser):
        """Reads the app configuration from a config parser object."""
        self.PING_URL = config["WEB"]["server"]

        self.UPDATE_TIME = config.getfloat("DISPLAY", "animation_rate")
        self.ASCII_ENABLED = config.getboolean("DISPLAY", "ascii_enabled")
        self.ASCII_FILE = config["DISPLAY"]["ascii_file"]

        self.SLEEP_TIME = config.getfloat("PREFERENCES", "sleep")
        self.FAIL_SLEEP_TIME = config.getfloat("PREFERENCES", "fail_sleep")
        self.MAX_FAILS = config.getint("PREFERENCES","max_fail")
        self.DISCONNECT_THRESHOLD = config.getint("PREFERENCES","disconnect_threshold")
        self.OPEN_BROWSER = config.getboolean("PREFERENCES", "open_browser")
        self.FALLBACK_MODE = config.getint("PREFERENCES","fallback_mode")

        self.REBOOT = config.getboolean("API", "reboot")

