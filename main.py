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
            if state.fail():
                myrouter.start()
        pong.play(SLEEP_TIME)


if __name__ == "__main__":
    properties.load()
    ping.URL = properties.get("PING_URL")
    ping.TIMEOUT = float(properties.get("TIMEOUT"))
    myrouter.COPY_TEXT = properties.get("PASSWORD")
    myrouter.URL = properties.get("URL")
    myrouter.BUFFER_LIFETIME = int(properties.get("BUFFER_LIFETIME"))
    SLEEP_TIME = float(properties.get("SLEEP_TIME"))
    UPDATE_TIME = float(properties.get("ANIMATION_UPDATE_TIME"))
    ASCII_ENABLED = properties.get_bool("ASCII_ENABLED")
    MAX_FAILS = int(properties.get("MAX_FAILS"))
    OPEN_ON_START: bool = properties.get_bool("OPEN_ON_START")
    ascii.load(ASCII_FILE)
    if OPEN_ON_START:
        myrouter.start()
    main()
