"""
The main script for the Ping application.

Pings some distant server at some time interval,
and (optionally) if the connection is absent during some
time, automatically opens the router page, passing down
the credentials for it to the clipboard buffer,
to quickly log in and reboot.

The "optional" and "some" settings may be changed
from the application.properties file.
"""
__version__ = "1.0.0"
__author__ = "MoonlightTaVi"


import util.properties as properties
import util.ascii as ascii
import src.ping as ping
import src.myrouter as myrouter
from util.animation import PingPong
from util.timer import Stopwatch
from util.state import State


SLEEP_TIME: float = 5
ASCII_FILE: str = "ascii_fu.txt"
UPDATE_TIME: float = 20
ASCII_ENABLED: bool = True
MAX_FAILS: int = 5
OPEN_BROWSER: bool = True
PING_URL: str = "google.com"


def ask_agreement() -> bool:
    inp: str = input("(Y/N) ").lower()
    while not inp in ['y', 'n']:
        inp = input("(Y/N) ").lower()
    return inp == 'y'

def should_open_page() -> bool:
    global OPEN_BROWSER
    print("Do you wish to open router page right now?")
    if not ask_agreement():
        print("Would you like me to open this page on disconnect (later)?")
        if not ask_agreement():
            OPEN_BROWSER = False
        return False
    return True


def main():
    stopwatch = Stopwatch()
    pong = PingPong(update_time=UPDATE_TIME)
    state = State()
    state.max_fails = MAX_FAILS
    while True:
        stopwatch.click()
        print(f"[{stopwatch.time()}]")
        if ping.ping():
            print(f"{ping.URL} is reachable. ({stopwatch.click()}s)")
            state.succeed()
        else:
            print(f"{ping.URL} is unreachable. ({stopwatch.click()}s)")
            if ASCII_ENABLED:
                ascii.draw(ASCII_FILE)
            if state.fail() and OPEN_BROWSER:
                myrouter.start()
        pong.play(SLEEP_TIME)

def show_logo():
    print('#' * 50)
    print(f"### PING-PONG v{__version__}")
    print(f"### \tby {__author__}")
    print(f"### \t\t*not sponsored by {PING_URL} ©")
    print('#' * 50)
    print()


if __name__ == "__main__":
    properties.load()
    PING_URL = properties.get("PING_URL")
    ping.URL = PING_URL
    ping.TIMEOUT = float(properties.get("TIMEOUT"))
    myrouter.COPY_TEXT = properties.get("PASSWORD")
    myrouter.URL = properties.get("URL")
    myrouter.BUFFER_LIFETIME = int(properties.get("BUFFER_LIFETIME"))
    SLEEP_TIME = float(properties.get("SLEEP_TIME"))
    UPDATE_TIME = float(properties.get("ANIMATION_UPDATE_TIME"))
    ASCII_ENABLED = properties.get_bool("ASCII_ENABLED")
    MAX_FAILS = int(properties.get("MAX_FAILS"))
    OPEN_BROWSER = properties.get_bool("OPEN_BROWSER")
    ascii.load(ASCII_FILE)
    show_logo()
    try:
        if should_open_page():
            myrouter.start()
        main()
    except KeyboardInterrupt:
        print("[SHUTDOWN]")
        input("Press any key to quit...")
