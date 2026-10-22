REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

from typing import Any

class ConfigError(Exception):
    """Raised when the configuration file is invalid."""


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


def check_required_keys(config: dict[str, str]) -> None:
         missing = []
         for key in REQUIRED_KEYS:
             if key not in config:
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


def parse_coordinates(config: dict[str, str], key: str,
                      width: int, height: int) -> tuple[int, int]:
    parts = config[key].split(",")
    if len(parts) != 2:
        raise ConfigError("should be two numbers, check ur chiffres")        # "needs two numbers: x,y"
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ConfigError(f"X and Y mus be integers, they aren't, got {config[key]}")
    if not (0 <= x < width):
        raise ConfigError(f"{key}: x must be between 0 and {width - 1}, got {x}")
    if not (0 <= y < height):
        raise ConfigError(f"{key}: y must be between 0 and {height - 1}, got {y}")
    return (x, y)


def parse_bool(config: dict[str, str], key: str) -> bool:
    value = config[key]
    if value == "True":
        return True
    if value == "False":
        return False
    raise ConfigError(f"{value} neither True or False")


def parse_output_file(config: dict[str, str], key: str) -> str:
    return config[key]


def load_config(path: str) -> dict[str, Any]:
    lines = read_config_file(path)
    config = parse_lines(lines)
    check_required_keys(config)

    width = parse_positive_int(config, "WIDTH")
    height = parse_positive_int(config, "HEIGHT")
    entry = parse_coordinates(config, "ENTRY", width, height)
    exit_ = parse_coordinates(config, "EXIT", width, height)
    if entry == exit_:
        raise ConfigError(f"ENTRY and EXIT must be different, both are {entry}")

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_,
        "output_file": parse_output_file(config, "OUTPUT_FILE"),
        "perfect": parse_bool(config, "PERFECT"),
    }
