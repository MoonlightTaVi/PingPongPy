import platform
import subprocess


TIMEOUT: float = 5
URL: str = "google.com"

def ping_server_subprocess(host: str, timeout: float = TIMEOUT):
    """
    Pings a host using the system's ping command 
    and returns a boolean indicating reachability.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Ping once
    command = ['ping', param, '1', host]
    try:
        output = subprocess.check_output(command, timeout=timeout)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def ping() -> bool:
    return ping_server_subprocess(URL)