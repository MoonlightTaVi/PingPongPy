
class State:
    # Open browser after some number of fails in a row
    fail_count: int = 0
    max_fails: int = 5
    # Do not open browser if already opened
    needs_reset: bool = False
    def fail(self) -> bool:
        self.fail_count += 1
        if self.fail_count >= self.max_fails and not self.needs_reset:
            self.needs_reset = True
            return True
        return False
    def succeed(self):
        self.fail_count = 0
        self.needs_reset = False