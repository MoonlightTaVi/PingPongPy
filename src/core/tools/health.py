"""
This module contains tools that can be used to check internet connection.
As of v1.0.0, it relies on the subprocess library.
"""
__version__ = "1.1.0"
__author__ = "MoonlightTaVi"


from configparser import ConfigParser
import os
import platform
import shutil
import subprocess


class PingSubprocess:
    """A tool that performs ping requests to a server through sub-processes."""

    def __init__(self) -> None:
        """Creates an instance of object with the default settings."""
        self.system_check() # Important!
        self.TIMEOUT: float = 5
        self.URL: str = "google.com"

    def ping_server_subprocess(self, host: str) -> bool:
        """
        Pings a host using the system's ping command 
        and returns a boolean indicating reachability.
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Ping once
        command = ['ping', param, '1', host]
        try:
            _ = subprocess.check_output(command, timeout=self.TIMEOUT)
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            return False
        
    def ping(self) -> bool:
        """
        Pings the default server (specified by config)
        and returns true if it is reachable; false otherwise.
        """
        return self.ping_server_subprocess(self.URL)
    
    def load_config(self, config: ConfigParser):
        """Loads the settings preset from a config."""
        self.URL = config["WEB"]["server"]
        self.TIMEOUT = config.getfloat("WEB", "TIMEOUT")
    
    def system_check(self):
        """Checks if the application can run on the current OS."""
        # The app uses the system 'ping' util
        full_path = shutil.which("ping")
        # Which can be missing
        if full_path is None:
            raise OSError("You don't have a ping.exe utility in your OS!")
        # Or the app may have the same name
        if not os.path.isabs(full_path):
            raise OSError("The application executable cannot be named 'ping.exe'")