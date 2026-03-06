"""
Time-relative utilities. 
May be used to track time, parse date/time to string, etc.
"""
__version__ = "1.0.0"
__author__ = "MoonlightTaVi"


from datetime import datetime


class Stopwatch:
    """A simple tool that tracks time passed between the click() calls."""

    def __init__(self) -> None:
        """Creates a new Stopwatch object."""
        self.dt = datetime.now()
        self.timestamp = self.dt.timestamp()

    def click(self, decimal_places: int = 3) -> float:
        """
        Resets the stopwatch time counter and returns the time passed
        since the last call, in milliseconds.
        Updates the current datetime.
        """
        dt = datetime.now()
        timestamp: float = dt.timestamp()
        time_passed: float = timestamp - self.timestamp
        self.timestamp = timestamp
        self.dt = dt
        return round(time_passed, decimal_places)
    
    def time(self) -> str:
        """
        Returns the datetime of the last click() call as a formatted string.
        """
        return self.dt.strftime("%H:%M:%S")