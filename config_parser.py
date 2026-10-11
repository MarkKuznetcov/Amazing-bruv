class ConfigError(Exception):
    """Raised when the configuration file is invalid."""

#encoding is the rules by which python turns bytes into text
def read_config_file(path: str) -> list[str]:
    try:
        with open(path, encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}")
# TODO: gérer aussi les autres erreurs possibles

def parse_lines(lines: list[str]) -> dict[str, str]:
    config: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        line = line.strip()
         for i in line:
            if line[i] ==" " or "#":
                i =+ 1

           try:
              with 
        # TODO 1: skip empty lines and comments
        # TODO 2: raise ConfigError if there is no "="
        #         include the line number in the message
        # TODO 3: split into key and value
        # TODO 4: store them in config
    return config