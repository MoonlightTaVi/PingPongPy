import os


class Reboot:
    """Runs shell command to reboot the router."""
    def __init__(self) -> None:
        self.url = ""
        self.endpoint = ""
        self.username = "admin"
        self.password = "admin"
        self.message = 'Rebooting the router, wait ~1 minute...'
    def full_url(self) -> str:
        """Returns full URL to reboot endpoint."""
        return f'{self.url}/{self.endpoint}'
    def get_auth(self) -> str:
        """Returns router credentials."""
        return f'{self.username}:{self.password}'
    def get_command(self) -> str:
        """Returns command (tested on Windows)."""
        return f'curl -s -o nul -w "{self.message}" --anyauth --user {self.get_auth()} -H "Referer: {self.url}" {self.full_url()}'
    def exec(self):
        """Reboots the router."""
        os.system(self.get_command())