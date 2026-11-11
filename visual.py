import os
from typing import Any

# top wall    -> "---"
#   no top wall -> "   "
# left wall    -> "|"
#   no left wall -> " "
# right wall    -> "|"
#   no right wall -> " "
# S  entry
# E  exit
# ·  shortest path
# █  closed 42-pattern cell
#   normal corridor

TOP_WALL = "---+"
TOP_OPEN = "   +"

LEFT_WALL = "|"
LEFT_OPEN = " "

BLOCKED_CELL = "█"
EMPTY_CELL = "   "
ENTRY_CELL = " S "
EXIT_CELL = " E "
PATH_CELL = " . "

COLOR_RESET = "\033[0m"

# 30 black
# 31 red
# 32 green
# 33 yellow
# 34 blue
# 35 magenta
# 36 cyan
# 37 white

# Wall > blocked > path also > S / E??
# THEMES = [
#     ("\033[37m", "\033[33m"),  # white
#     ("\033[32m", "\033[35m"),  # green
#     ("\033[33m", "\033[31m"),  # yellow
# ]

ENTRY_COLOR = "\033[35m"
EXIT_COLOR = "\033[31m"
BLOCKED_COLOR = "\033[33m"
PATH_COLOR = "\033[36m"
ERROR_COLOR = "\033[31m"

# duh way clearer
THEMES = [
    {   # Default
        "wall": "\033[37m",
        "blocked": "\033[34m",
    },
    {   # Green
        "wall": "\033[32m",
        "blocked": "\033[33m",
    },
    {   # Red
        "wall": "\033[31m",
        "blocked": "\033[37m",
    },
    {   # Cyan
        "wall": "\033[36m",
        "blocked": "\033[35m",
    },
    {   # Grey
        "wall": "\033[33m",
        "blocked": "\033[31m",
    },
    {   # Grey
        "wall": "\033[30m",
        "blocked": "\033[32m",
    },
]


def render_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]],
    blocked: set[int],
    theme_index: int = 0,
) -> None:
    north = 1
    east = 2
    south = 4
    west = 8

    height = len(grid)
    width = len(grid[0])

    theme = THEMES[theme_index]

    wall_color = theme["wall"]
    blocked_color = theme["blocked"]
    # path_color = theme["path"]
    # entry_color = theme["entry"]
    # exit_color = theme["exit"]

    for y in range(height):
        top_line = colorize("+", wall_color)
        cell_line = ""

        for x in range(width):
            cell = grid[y][x]
            cell_id = y * width + x

            # Create cell content
            if cell & north:
                top_line += colorize(TOP_WALL, wall_color)
            else:
                top_line += colorize(TOP_OPEN, wall_color)

            if cell & west:
                cell_line += colorize(LEFT_WALL, wall_color)
            else:
                cell_line += colorize(LEFT_OPEN, wall_color)

            # Add the cell content
            if cell_id in blocked:
                cell_line += colorize(BLOCKED_CELL * 3, blocked_color)
            elif (x, y) == entry:
                cell_line += colorize(ENTRY_CELL, ENTRY_COLOR)
                # TODO change to theme later
            elif (x, y) == exit_:
                cell_line += colorize(EXIT_CELL, EXIT_COLOR)
                # TODO change to theme later
            elif (x, y) in path:
                cell_line += colorize(PATH_CELL, PATH_COLOR)
                # TODO change to theme later
            else:
                cell_line += EMPTY_CELL

        if grid[y][width - 1] & east:
            cell_line += colorize(LEFT_WALL, wall_color)
        else:
            cell_line += colorize(LEFT_OPEN, wall_color)
        print(top_line)
        print(cell_line)

    bottom_line = colorize("+", wall_color)
    for x in range(width):
        cell = grid[height - 1][x]

        if cell & south:
            bottom_line += colorize(TOP_WALL, wall_color)
        else:
            bottom_line += colorize(TOP_OPEN, wall_color)

    print(bottom_line)


def path_to_cells():
    """Convert the shortest path into coordinates."""
    pass


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{COLOR_RESET}"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_menu(
    generator: Any,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    path: list[tuple[int, int]] | None = None,
) -> None:
    path_cells = path if path is not None else []
    theme_index = 0
    show_path = False
    error_message = ""
    grid = generator.grid

    while True:
        clear_screen()
        render_maze(
            grid=grid,
            entry=entry,
            exit_=exit_,
            path=path_cells if show_path else [],
            blocked=generator.blocked,
            theme_index=theme_index,
        )

        if error_message:
            print("\n" + colorize(error_message, ERROR_COLOR))
            error_message = ""

        print("\n1. Regenerate maze")
        print("2. Show/hide shortest path")
        print("3. Change colors")
        print("4. Quit")

        choice = input("Choice: ").strip()

        if choice == "1":
            grid = generator.generate(perfect)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4":
            return
        else:
            error_message = "Invalid choice. Please select 1, 2, 3, or 4."
