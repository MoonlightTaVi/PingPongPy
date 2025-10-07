from datetime import datetime

class Stopwatch:
    def __init__(self) -> None:
        self.dt = datetime.now()
        self.timestamp = self.dt.timestamp()
    def click(self, decimal_places: int = 3) -> float:
        dt = datetime.now()
        timestamp: float = dt.timestamp()
        time_passed: float = timestamp - self.timestamp
        self.timestamp = timestamp
        self.dt = dt
        return round(time_passed, decimal_places)
    def time(self) -> str:
        return self.dt.strftime("%H:%M:%S")