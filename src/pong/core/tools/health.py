"""
This module contains tools that can be used to check internet connection.
As of v1.0.0, it relies on the subprocess library.
"""
__version__ = "1.3.0"
__author__ = "MoonlightTaVi"


from abc import ABC, abstractmethod
from configparser import ConfigParser
import os
import platform
import shutil
import subprocess

import requests


class PingUtil(ABC):
    """The utility that checks the Internet connection state."""

    def __init__(self) -> None:
        """Creates an instance of object with the default settings."""
        self.TIMEOUT: float = 5
        self.URL: str = "google.com"
    
    def load_config(self, config: ConfigParser):
        """Loads the settings preset from a config."""
        self.URL = config["WEB"]["server"]
        self.TIMEOUT = config.getfloat("WEB", "TIMEOUT")
    
    @abstractmethod
    def ping(self) -> bool:
        """
        Pings the remote server and  returns True
        if the server responds; 
        False may indicate that either the Internet conncetion is missing
        OR the server is down.
        """
        ...
    


class PingSubprocess(PingUtil):
    """A tool that performs ping requests to a server through sub-processes."""

    def __init__(self) -> None:
        """Creates an instance of object with the default settings."""
        super(PingSubprocess, self).__init__()
        self.system_check() # Important!
    
    def ping(self) -> bool:
        return self.ping_server_subprocess(self.URL)

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


class PingRequest(PingUtil):
    """This implementation of PingUtil relies on the 'requests' module."""

    def ping(self) -> bool:
        response = requests.get(self.URL, timeout=self.TIMEOUT)
        return response.status_code == 200