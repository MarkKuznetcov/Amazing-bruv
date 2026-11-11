import sys

from all_before.config_parser import load_config
from maze import Mazegenerator
from visual import display_menu


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    config = load_config("all_before/config.txt")

    generator = Mazegenerator(
        config["width"],
        config["height"],
        config["seed"],
    )

    grid = generator.generate(config["perfect"])
    path = generator.solve(config["entry"], config["exit"])

    display_menu(
        generator=generator,
        entry=config["entry"],
        exit_=config["exit"],
        perfect=config["perfect"],
        path=path,
    )


if __name__ == "__main__":
    main()
