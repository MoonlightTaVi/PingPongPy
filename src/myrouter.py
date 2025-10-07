import tkinter as tk
import webbrowser


COPY_TEXT: str = "admin"
URL: str = "http://192.168.0.1/"
BUFFER_LIFETIME: int = 300


def copy_to_clipboad(text: str = COPY_TEXT):
    """Copy the specified text to clipboard"""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.after(BUFFER_LIFETIME, root.destroy)
    root.mainloop()

def open_browser(url: str = URL):
    """Open URL in the default browser"""
    webbrowser.open(url)


def start():
    """Copy router password and open in browser."""
    copy_to_clipboad()
    open_browser()


### Launch on click
if __name__ == "__main__":
    start()