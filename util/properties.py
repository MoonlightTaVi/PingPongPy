from configparser import ConfigParser


pairs: dict = {}
data_folder: str = "data"

config = ConfigParser()


def load() -> dict:
    """
    Reads application.properties and returns dict of
    property pairs (key:value).
    If the properties are already loaded, just returns them.

    Deprecated.
    """
    global pairs
    if len(pairs) > 0:
        return pairs
    print("Loading properties...")
    with open(f"{data_folder}/application.properties", 'r') as f:
        while True:
            line: str = f.readline().strip()
            print(line)
            if line == "":
                break
            pair:list = line.split("=")
            pairs[pair[0]] = pair[1]
    return pairs


def load_config() -> ConfigParser:
    """
    Reads CONFIG.INI and returns dict of
    property pairs (key:value).
    If the properties are already loaded, just returns them.
    """
    global config
    config.read(f"{data_folder}/CONFIG.INI")
    return config


def get(key: str, default_value: str = "") -> str:
    """
    Get value, assigned to the key,
    if it exists. Otherwise default value.

    Deprecated.
    """
    if not key in pairs:
        return default_value
    return pairs[key]

def get_bool(key: str) -> bool:
    """
    Get value, assigned to the key,
    if it exists. Otherwise default value.
    
    Deprecated.
    """
    bool_str: str = get(key,"false")
    return bool_str.lower() == "true"