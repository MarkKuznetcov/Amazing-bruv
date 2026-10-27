import sys

from config_parser import ConfigError, load_config


def main() -> None:
    if len(sys.argv) != 2:
        print("There are less, or more than 2 arguments", file=sys.stderr)
        sys.exit(1)
    config_name = sys.argv[1]
    try:
        config = load_config(config_name)
    except ConfigError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"so the config is: {config}") # a remplace later bruv


if __name__ == "__main__":
    main()