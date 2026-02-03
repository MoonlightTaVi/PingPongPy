"""
Base Ping-Pong application classes that manage the whole life cycle
of the programm.
"""
__version__ = "1.2.0"
__author__ = "MoonlightTaVi"


from configparser import ConfigParser
import sys

from .util.art import PingPongAnim, AsciiDrawer
from .util import messages
from .util.metrics import Stopwatch
from .tools.browser import BrowserPage
from .tools.health import PingSubprocess
from .tools.shell import ShellReboot
from .config import ConfigReader, AppConfig


def format_red(text: str) -> str:
    """Colors the text RED (for the terminal output)."""
    return f'\u001B[91m{text}\u001B[0m'

def format_yellow(text: str) -> str:
    """Colors the text YELLOW (for the terminal output)."""
    return f'\u001B[93m{text}\u001B[0m'

def format_green(text: str) -> str:
    """Colors the text GREEN (for the terminal output)."""
    return f'\u001B[92m{text}\u001B[0m'


class State:
    """Stores the current internet connection health check state."""
    def __init__(self):
        # Open browser after some number of fails in a row
        self.fail_count: int = 0
        self.max_fails: int = 5
        # Reboot again if the connection isn't regained
        #  after this number of failures
        self.disconnect_threshold: int = 15
        # Cannot reboot more than this number of times consequently
        self.reboot_count: int = 0
        self.max_reboots: int = 3 # Can't be changed in config

        # Do not open browser if already opened
        # Do not open unless succeeded at least once after startup
        self.disconnected: bool = False

    def can_reboot(self) -> bool:
        """
        Counts a single internet connection check failure.
        Returns true if have failed a few times, and the router must be
        rebooted. False otherwise 
        (it may be a micro-disconnect or a complete connection loss).
        """
        self.fail_count += 1
        if self.fail_count >= self.max_fails and not self.disconnected:
            self.disconnected = True
            return True
        return False
    
    def can_reset(self) -> bool:
        """
        Returns True if the router can be tried to reboot once again.
        
        If the connection is completely lost, by default the app will try
        to reboot yet 3 times until giving up completely.
        """
        return self.reboot_count < self.max_reboots
    
    def reset(self) -> None:
        """
        Resets the fail count and increments the reboot count, 
        so that the app can try to reboot again.
        """
        self.reboot_count += 1
        self.fail_count = 0
        self.disconnected = False
    
    def succeed(self):
        """
        Marks the internet connection as 'stable'
        and resets the failure counter.
        """
        self.reboot_count = 0
        self.fail_count = 0
        self.disconnected = False
    
    def is_connection_lost(self):
        """
        Returns true if the remote server 
        does not respond for a long time.
        """
        return self.fail_count >= self.disconnect_threshold
    
    def __str__(self) -> str:
        """Returns the current state, formatted to a string."""
        # Defaults to 'connected'
        state: str = format_green('[OK]')
        threshold: int = self.max_fails
        # Fatal disconnect
        if self.fail_count > self.max_fails:
            state = format_red('[DC]')
            threshold = self.disconnect_threshold
        # Micro disconnect
        elif self.fail_count != 0:
            state = format_yellow('[FAIL]')
        
        state = f'{state}: {self.fail_count}/{threshold}'
        retry = f'[RETRY] {self.reboot_count}/{self.max_reboots}'

        return '\n\t'.join(['<State>:', state, retry])


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
        self.state.max_fails = self.config.MAX_FAILS
        self.state.disconnect_threshold = self.config.DISCONNECT_THRESHOLD

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
                # Open router page (basic mode)
                if self.config.OPEN_BROWSER:
                    self.browser.start()
                # Reboot via curl request (advanced mode)
                elif self.config.REBOOT:
                    self.reboot.exec()
            
            # If the connection is completely lost
            elif self.state.is_connection_lost():
                # Whether to prompt to reboot manually
                go_idle: bool = False
                if self.config.FALLBACK_MODE == 1:
                    go_idle = True
                # Try to reboot automatically
                elif self.config.FALLBACK_MODE == 2:
                    # If can reset the reboot count, do it
                    if self.state.can_reset():
                        self.state.reset()
                    # But can't do that eternally (switch to fallback mode 1)
                    else:
                        go_idle = True
                # May ask user to reboot manually in any case
                if go_idle:
                    self.idle_mode()
                # Or just do nothing... (keep pinging)
        
        # Print state
        print(self.state)

        # Wait for some time, based on whether the connection is stable
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
                sys.exit()

            # The internet connection issue is fixed
            connection_established = True

        # Mark the connection as stable
        self.state.succeed()