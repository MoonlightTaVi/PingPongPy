"""
Tools for command line GUI: ASCII graphics, simple idle animations, etc.
"""
__version__ = "1.1.0"
__author__ = "MoonlightTaVi"


from datetime import datetime
import time


class AsciiDrawer:
    """A small util for drawing ASCII images to the console."""
    def __init__(self, data_folder: str = "data") -> None:
        """
        Initializes an empty ASCII drawer 
        using the given data directory for image files.
        """
        self.images = {}
        self.data_folder = data_folder

    def load(self, filename: str) -> str:
        """Loads a single ASCII drawing from a file."""
        drawing: str
        with open(f"{self.data_folder}/{filename}", 'r') as f:
            drawing = f.read()
        self.images[filename] = drawing
        return drawing
    
    def get_image(self, filename: str) -> str:
        """Returns a drawing as plain text; loads it if it wasn't loaded yet."""
        if not filename in self.images:
            return self.load(filename)
        else:
            return self.images[filename]
        
    def draw(self, filename: str):
        """Prints a cached ASCII drawing (loaded from a file) to the console."""
        drawing: str = self.get_image(filename)
        print(drawing)


class PingPongAnim:
    """Used to pause app execution and play ping-pong animation."""
    state: int = 0
    blink: bool = False

    def __init__(
            self, 
            width: int = 8, 
            update_time: float =  0.2
            ) -> None:
        self.width = width
        self.update_time = update_time
    
    def __timestamp(self) -> float:
        return datetime.now().timestamp()

    def play(self, duration: float = 5):
        """
        Pause execution and play ping-pong animation.

        The 'blink' variable of the object may be optionally set to True
        to enable color blinking.
        
        Parameters
        ----------
            duration: float = 5
                Time until the animation is stopped, in seconds.
            update_time: float = 0.13
                Time until the next frame. The lower the value,
                the faster the animation.
        """

        start_time: float = self.__timestamp()
        # The pong ball counts as 1 of width,
        #  so reduce the overall width by 1
        width: int = self.width - 1
        while True:
            time.sleep(self.update_time)
            if self.__timestamp() - start_time >= duration:
                break
            self.state += 1
            state: int = self.state % (width * 2)
            if state > width:
                state = width - self.state % width
            left: str = "*" * state
            right: str = "*" * (width - state)
            self.__print("[" + left + "O" + right + "]")
    
    def __print(self, text: str):
        """Prints the animation to the console."""
        # Blink every uneven frame (if enabled)
        if self.blink and self.state % 2 == 1:
            text = f'\u001B[93m{text}\u001B[0m'
        
        print(text, end='\r')