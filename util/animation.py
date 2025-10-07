from datetime import datetime
import time

UPDATE_TIME: float = 0.2


def timestamp() -> float:
    return datetime.now().timestamp()

class PingPong:
    """Used to pause app execution and play ping-pong animation."""
    state: int = 0
    def __init__(
            self, 
            width: int = 8, 
            update_time: float = UPDATE_TIME
            ) -> None:
        self.width = width
        self.update_time = update_time
    def play(self, duration: float = 5):
        """Pause execution and play ping-pong animation.
        
        Parameters
        ----------
            duration: float = 5
                Time until the animation is stopped, in seconds.
            update_time: float = 0.13
                Time until the next frame. The lower the value,
                the faster the animation.
        """
        start_time: float = timestamp()
        # The pong ball counts as 1 of width,
        #  so reduce the overall width by 1
        width: int = self.width - 1
        while True:
            time.sleep(self.update_time)
            if timestamp() - start_time >= duration:
                break
            self.state += 1
            state: int = self.state % (width * 2)
            if state > width:
                state = width - self.state % width
            left: str = "*" * state
            right: str = "*" * (width - state)
            print("[" + left + "O" + right + "]", end='\r')


#PingPong().play()