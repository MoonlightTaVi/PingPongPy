"""
The main script for the Ping-Pong application.

Pings some distant server at some time interval,
and (optionally), if the connection is absent during some
time, automatically opens the router page passing down
the credentials for it to the clipboard buffer
to quickly log in and reboot.

The "optional" and "some" settings may be changed
from the application.properties file.
"""
__version__ = "3.1.1"
__author__ = "MoonlightTaVi"


import multiprocessing

from core.app import PingPong


def show_logo():
    print('#' * 50)
    print(f"### PING-PONG v{__version__}")
    print(f"### \tby {__author__}")
    print('#' * 50)
    print()


def run():
    app = PingPong()
    app.load_config()
    while True:
        app.run()

def main():
    show_logo()

    try:
        run()
    except KeyboardInterrupt: # Ctrl+C quits the application
        print("[SHUTDOWN]")
    except Exception as e:
        print(f'[Uncaught exception] {e}')
    
    input("Press Enter to quit...")



if __name__ == "__main__":
    multiprocessing.freeze_support() # Infinite process spawning issue
    main()
