from all_before.config_parser import load_config
from maze import Mazegenerator
from visual import render_maze


def main() -> None:
    config = load_config("all_before/config.txt")

    generator = Mazegenerator(
        config["width"],
        config["height"],
        config["seed"],
    )

    grid = generator.generate(config["perfect"])

    render_maze(
        grid=grid,
        entry=config["entry"],
        exit_=config["exit"],
        path=[],
        blocked=generator.blocked,
    )


if __name__ == "__main__":
    main()
