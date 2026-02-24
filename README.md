A command line application that automatically reboots the router
upon a WAN disconnect by running `curl` to the specified router page end-point.

The settings may be configured to work in a number of different modes.

# Why

Originally, I made a small script for the personal usage;
my ISP (Internet Service Provider) gives me a lot of connection outages.
Usually those are micro-disconnects, but my old TP-LINK router can't recover
from them: it needs a reboot every time this happens.

The first version of the script was really simple: it used to open the router
page and automatically copy the password to the router when a remote server
does not respond to a `ping`.

But that was not sufficient, and at some point I had to reverse-engineer the
router HTML page in order to find out: what actually happens when you click
the "Reboot" button.

Now, this is a complete tool that can become useful to any person,
not just me.

# How it works

- The app `ping`s the specified server; when the server does not respond for
some time, it launches the "recovering" process;
- Each Internet router has its IP address; it also has some HTM end-point
with a script that starts the router rebooting process;
- The app makes a simple POST request to this end-point, passing 
the required authentification credentials along with it;
- If the connection is not recovered after some time, the app may try rebooting
the router again.

# Modes

Not all Internet routers follow the same structure:
- The router IP addresses may vary;
- The "Reboot" end-points may vary;
- And literally anything may vary.

If the only problems are the 1st and the 2nd, the required HTTP address
may be configured in the `CONFIG.INI` file.

In the worst case scenario, the application may be used in the legacy mode,
which means: simply open the router page upon a disconnect.

The application may even be used to simply ping the connection continuously,
without performing any "recover" logic 
(though using a CLI for this goal is not the best idea).

# Warnings

1. Your router credentials are safe to expose **as long as your router is not
exposed to the WEB** (by default it isn't). 
But the application uses it internally anyway.
2. The application is made on Windows and **is designed for Windows**. It may
work on UNIX, but I do not promise it; it wasn't tested. To run on Linux/MacOS,
the binary must be compiled manually 
(or you can simply run the `src/main.py` script).
3. The executable may have any name, but it **cannot be named `ping.exe`**.
Thankfully, since v3.x.x the application won't start when it has such a name.

# Settings

Many various settings may be changed in the `data/CONFIG.INI` file.
Here are the most useful ones:

- `open_browser` specifies the mode:
    - `0` will try to automatically reboot the router;
    - `1` is the legacy mode that opens the router page for a manual reboot;
- `reboot` also the specifies the mode:
    - `0` will do **nothing** at all (even when `open_browser=0`);
    - `1` will enable the automatical reboot mode;
- `copy` (when enabled) will override the clipboard buffer with the password to the router upon a disconnect;
- `ascii_enabled` is a legacy feature, so called "myopia mode":
    - Use `1` to enable and `0` to disable;
    - When enabled, prints a giant "F*** YOU" ASCII image to the console;
    - Its purpose is to notify the user about the connection state when they are AFK (the image can be seen from afar);
    - The image may be changed using the `ascii_file` property;
    - The latest versions use the colored text for this purpose: the application will blink with yellow instead of drawing ASCII.
- `URL` is the router IP address;
- `endpoint` is the router "Reboot" end-pont (only for the automatical reboot mode);
- `server` is a web address that will be `ping`ed to check the connection status;
- `username` and `password` are credentials for the router page.

# Features

- Since v3.x.x, the application can reboot the router **three times** in a row if the connection cannot be recovered easily. Afterwards, the user must manually type `y` to try rebooting again.
- The application always checks the connection state first, and only then it starts the rebooting. Exception: the specified server may not respond even if the connection is otherwise stable. There is no way to set the second "fallback" option for a server (sorry).
- Pressing `Ctrl+C` will quit the application. But pressing `Ctrl+C` two times will throw an exception, don't do that.

# Contribution

Anyone can participate in the development of this project, for example:

- Compile and test the build for UNIX systems;
- Add missing functionality;
- Fix bugs that I don't know about yet.

But beware: I hate Python, and the code is an unreadable mess.

# Licence

BSD-2-Clause license means "do whatever you want, I don't care".
Use code snippets, modify the code, sell the application on CDs; just
don't forget to leave the same LICENSE file in your distributions.