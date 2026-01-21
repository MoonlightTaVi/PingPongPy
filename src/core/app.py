"""
Base Ping-Pong application classes that manage the whole life cycle
of the programm.
"""
__version__ = "1.1.0"
__author__ = "MoonlightTaVi"


from configparser import ConfigParser

from .util.art import PingPongAnim, AsciiDrawer
from .util import messages
from .util.metrics import Stopwatch
from .tools.browser import BrowserPage
from .tools.health import PingSubprocess
from .tools.shell import ShellReboot
from .config import ConfigReader, AppConfig


class State:
    """Stores the current internet connection health check state."""
    def __init__(self):
        # Open browser after some number of fails in a row
        self.fail_count: int = 0
        self.max_fails: int = 5
        # Do not open browser if already opened
        # Do not open unless succeeded at least once after startup
        self.needs_reset: bool = False

    def can_reboot(self) -> bool:
        """
        Counts a single internet connection check failure.
        Returns true if have failed a few times, and the router must be
        rebooted. False otherwise 
        (it may be a micro-disconnect or a complete connection loss).
        """
        self.fail_count += 1
        if self.fail_count >= self.max_fails and not self.needs_reset:
            self.needs_reset = True
            return True
        return False
    
    def succeed(self):
        """
        Marks the internet connection as 'stable'
        and resets the failure counter.
        """
        self.fail_count = 0
        self.needs_reset = False
    
    def connection_lost(self):
        """
        Returns true if the remote server 
        does not respond for a long time.
        """
        return self.fail_count >= self.max_fails * 2


class PingPong:
    """
    The main PingPong application class. 
    Manages the lifecycle of the program.
    """

    def __init__(self):
        """Instantiates a new PingPong with the deafult configuration."""
        self.config = AppConfig()
        self.browser = BrowserPage()
        self.page = BrowserPage()
        self.process = PingSubprocess()
        self.reboot = ShellReboot()
        self.state = State()
        self.stopwatch = Stopwatch()
        self.pong = PingPongAnim()
        self.ascii = AsciiDrawer()

    def load_config(self):
        """
        Loads and reads all the app configuration from the CONFIG.INI file.
        """
        reader = ConfigReader()
        parser: ConfigParser = reader.get_config()
        self.config.load_config(parser)
        self.browser.load_config(parser)
        self.page.load_config(parser)
        self.process.load_config(parser)
        self.reboot.load_config(parser)
        self.ascii.load(self.config.ASCII_FILE)
        self.pong.update_time = self.config.UPDATE_TIME

    def run(self):
        """
        Performs a single iteration of the application functionality.

        Pings the specified server; reboots the router or opens the router
        page when needed. Also plays the idle animation and prints ASCII art,
        if enabled.
        """

        self.stopwatch.click()
        print(f"[{self.stopwatch.time()}]")
        if self.process.ping():
            print(f"{self.process.URL} is reachable. ({self.stopwatch.click()}s)")
            self.state.succeed()

        else:
            print(f"{self.process.URL} is unreachable. ({self.stopwatch.click()}s)")
            if self.config.ASCII_ENABLED:
                self.ascii.draw(self.config.ASCII_FILE)
            
            # Try rebooting automatically
            if self.state.can_reboot():
                if self.config.OPEN_BROWSER:
                    self.browser.start()
                elif self.config.REBOOT:
                    self.reboot.exec()
            # Ask to reboot manually or quit
            else:
                self.idle_mode()
        
        sleep: float
        if self.state.fail_count == 0:
            sleep = self.config.SLEEP_TIME
        else:
            sleep = self.config.FAIL_SLEEP_TIME
        
        self.pong.play(sleep)
    
    def idle_mode(self):
        """
        Enters the idle mode, where the user is asked to reboot the router
        manually or quit the application.
        The 'while True' will end once the connection is re-established.
        """

        print("It seems that the connection has been lost")
        print(" and cannot be recovered.")
        print("From now on, you need to either reboot the router manually")
        print(" or just give up.")

        connection_established = False
        while not connection_established:
            # Reboot
            if messages.ask("Do you want to reboot again?"):
                self.reboot.exec()
                if not self.process.ping():
                    # Keep rebooting
                    continue
            # Give up
            else:
                quit()

            # The internet connection is fixed
            connection_established = True