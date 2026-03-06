"""
This module contains utilities for the Internet router rebooting.
"""
__version__ = "1.3.0"
__author__ = "MoonlightTaVi"


from abc import ABC, abstractmethod
from configparser import ConfigParser
import time

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from .shell import ShellReboot


class RebootUtil(ABC):
    """Base abstract class for router rebooting."""

    def __init__(self) -> None:
        self.url = ""
        self.endpoint = ""
        self.username = "admin"
        self.password = "admin"
        self.message = 'Rebooting the router, wait ~1 minute...'

    def full_url(self) -> str:
        """Returns full URL to reboot endpoint."""
        return f'{self.url}/{self.endpoint}'
    
    def load_config(self, config: ConfigParser):
        """Loads the settings preset from a config."""
        self.username = config["API"]["username"]
        self.password = config["API"]["password"]
        self.url = config["API"]["URL"]
        self.endpoint = config["API"]["endpoint"]

    @abstractmethod
    def start(self) -> bool:
        """Launches the reboot process. Returns True on success."""
        ...


class ShellRebootAdapter(RebootUtil):
    """An adapter for the legacy ShellReboot class."""

    def __init__(self) -> None:
        self.reboot = ShellReboot()
    
    def start(self) -> bool:
        print(self.message)
        self.reboot.exec()
        time.sleep(10)
        return True

    def load_config(self, config: ConfigParser):
        return self.reboot.load_config(config)
    

class RequestReboot(RebootUtil):
    """This implementation of RebootUtil relies on the 'requests' library."""
    session = requests.Session()

    def __init__(self) -> None:
        super(RequestReboot, self).__init__()
    
    def load_config(self, config: ConfigParser):
        super(RequestReboot, self).load_config(config)
        self.session.headers.update({"Referer": self.url})

    def start(self) -> bool:
        auth = HTTPBasicAuth(self.username, self.password)
        response = self.session.get(self.full_url(), auth=auth)
        if response.status_code == 200:
            print(self.message)
            time.sleep(10)
        else:
            print(f'Auth failed: {response.status_code}')
        
        return response.status_code == 200