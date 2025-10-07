import platform
import subprocess

import myrouter
import util.properties as properties
import util.ascii as ascii
from util.timer import Stopwatch
from util.animation import PingPong

### Setup
properties.load()
if properties.get_bool("OPEN_ON_START"):
    myrouter.run()
display_ascii: bool = properties.get_bool("ASCII_ENABLED")
target_host = properties.get("PING_URL", "google.com")
MAX_FAILS: int = int(properties.get("MAX_FAILS"))
TIMEOUT: float = float(properties.get("TIMEOUT"))
SLEEP_TIME: float = float(properties.get("SLEEP_TIME"))
UPDATE_TIME: float = float(properties.get("ANIMATION_UPDATE_TIME"))


def ping_server_subprocess(host: str, timeout: float = TIMEOUT):
    """
    Pings a host using the system's ping command 
    and returns a boolean indicating reachability.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Ping once
    command = ['ping', param, '1', host]
    try:
        # 5-second timeout
        output = subprocess.check_output(command, timeout=timeout)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False


### Main

stopwatch: Stopwatch = Stopwatch()

def loop():
    """
    Check Internet connection in a loop
    and open router page if connection
    is absent for MAX_FAILS * SLEEP_TIME seconds
    (router page will open once again
    only after the connection will be re-stabilized).

    Use to reboot the router.
    """
    # Open browser after some number of fails in a row
    fail_count: int = 0
    # Do not open browser if already opened
    browser_opened: bool = False
    # 
    pong: PingPong = PingPong(update_time=UPDATE_TIME)

    while True:
        stopwatch.click()
        print(f"[{stopwatch.time()}]")
        if ping_server_subprocess(target_host):
            print(f"{target_host} is reachable. ({stopwatch.click()}s)")
            # Reset
            fail_count = 0
            browser_opened = False
        else:
            print(f"{target_host} is unreachable. ({stopwatch.click()}s)")
            # (Myopia Mode)
            # Nuke ASCII drawing, so that DC is seen from afar
            if display_ascii:
                ascii.draw("ascii_fu.txt")
            fail_count += 1
            if fail_count >= MAX_FAILS and not browser_opened:
                print("Opening router page...")
                browser_opened = True
                myrouter.run()

        pong.play(SLEEP_TIME)


### Run app
if __name__ == "__main__":
    loop()