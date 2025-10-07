import tkinter as tk
import webbrowser
import util.properties as properties


properties.load()
COPY_TEXT: str = properties.get("PASSWORD")
URL: str = properties.get("URL")
BUFFER_LIFETIME: int = int(properties.get("BUFFER_LIFETIME"))


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


def run():
    """Copy router password and open in browser."""
    copy_to_clipboad()
    open_browser()


### Launch on click
if __name__ == "__main__":
    run()