REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


#encoding is the rules by which python turns bytes into text
def read_config_file(path: str) -> list[str]:
    try:
        with open(path, encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        raise ConfigError(f"Config file not found in: {path}")
    except IsADirectoryError:
        raise ConfigError(f"{path} is a directory, not a file bruv")
    except PermissionError:
        raise ConfigError(f"You dont have permission to read this {path}")
    except UnicodeDecodeError:
        raise ConfigError(f"{path} The file bytes aren't valid UTF-8 text")
    except OSError as e:
        raise ConfigError(f"Cannot read '{path}': {e}")


def parse_lines(lines: list[str]) -> dict[str, str]:
    config: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"Line {number} is missing '=' not in {line} bruv")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key == "":
            raise ConfigError(f"Line {number}: empty key")
        if value == "":
            raise ConfigError(f"Line {number}: empty value")
        if key in config:
            raise ConfigError(f"Line {number}: duplicated key '{key}'")
        config[key] = value
    return config


for path in ["config.txt", "nope.txt", "."]:
         try:
             print("OK   ", read_config_file(path))
         except ConfigError as e:
             print("ERROR", e)
 
 
def check_required_keys(config: dict[str, str]) -> None:
         missing = []
         for key in REQUIRED_KEYS:
             if key not in REQUIRED_KEYS:
                 missing.append(key)
         if missing:
             raise ConfigError(f"Missing keys: {', '.join(missing)}")
 
 
def parse_positive_int(config: dict[str, str], key: str) -> int:
         try:
             number = int(config[key])
         except ValueError:
             raise ConfigError(f"{key} is not an entier")
         if number <= 0:
             raise ConfigError(f"{key} must be greater than 0, got {number}")
         return number

    
if __name__ == "__main__":
    def check(lines: list[str]) -> None:
        try:
            print("OK   ", parse_lines(lines))
        except ConfigError as e:
            print("ERROR", e)


    check(["# comment\n", "WIDTH=20\n", "\n", "HEIGHT=15\n"])
    check(["WIDTH = 20\n"])          # spaces around the = are cleaned
    check([])                        # empty file gives {}


    check(["WIDTH 20\n"])            # no =
    check(["=20\n"])                 # empty key
    check(["WIDTH=\n"])              # empty value
    check(["WIDTH=20\n", "WIDTH=30\n"])   # duplicate key

    good = {"WIDTH": "20", "HEIGHT": "15", "ENTRY": "0,0",
        "EXIT": "19,14", "OUTPUT_FILE": "maze.txt", "PERFECT": "True"}

    check_required_keys(good)              # ne doit rien afficher ni lever
    check_required_keys({"WIDTH": "20"})   # doit lister HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT