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
ERROR_COLOR = "\033[31m"

PATH_CHARS = {
    frozenset(("N", "S")): "│",
    frozenset(("E", "W")): "─",
    frozenset(("N", "E")): "└",
    frozenset(("N", "W")): "┘",
    frozenset(("S", "E")): "┌",
    frozenset(("S", "W")): "┐",
}

# Thicker characters
# PATH_CHARS = {
#     frozenset(("N", "S")): "║",
#     frozenset(("E", "W")): "═",
#     frozenset(("N", "E")): "╚",
#     frozenset(("N", "W")): "╝",
#     frozenset(("S", "E")): "╔",
#     frozenset(("S", "W")): "╗",
# }

# duh way clearer
THEMES = [
    {   # Default
        "wall": "\033[37m",
        "blocked": "\033[34m",
        "path": "\033[31m",
    },
    {   # Green
        "wall": "\033[32m",
        "blocked": "\033[33m",
        "path": "\033[33m",
    },
    {   # Red
        "wall": "\033[31m",
        "blocked": "\033[37m",
        "path": "\033[37m",
    },
    {   # Cyan
        "wall": "\033[36m",
        "blocked": "\033[35m",
        "path": "\033[35m",
    },
    {   # Grey
        "wall": "\033[33m",
        "blocked": "\033[31m",
        "path": "\033[31m",
    },
    {   # Grey
        "wall": "\033[30m",
        "blocked": "\033[32m",
        "path": "\033[32m",
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
    path_symbols = path_to_symbols(path)

    wall_color = theme["wall"]
    blocked_color = theme["blocked"]
    path_color = theme["path"]
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
            elif (x, y) in path_symbols:
                symbol = path_symbols[(x, y)]
                cell_line += colorize(f" {symbol} ", path_color)
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


def path_to_cells(
    entry: tuple[int, int],
    path: list[str],
) -> list[tuple[int, int]]:
    x, y = entry
    cells = [(x, y)]

    for direction in path:
        if direction == "N":
            y -= 1
        elif direction == "E":
            x += 1
        elif direction == "S":
            y += 1
        elif direction == "W":
            x -= 1

        cells.append((x, y))

    return cells


def path_to_symbols(path: list[tuple[int, int]]) -> dict:
    symbols = {}

    for i, (x, y) in enumerate(path):
        connections = set()

        if i > 0:
            px, py = path[i - 1]
            connections.add(get_direction(x, y, px, py))

        if i < len(path) - 1:
            nx, ny = path[i + 1]
            connections.add(get_direction(x, y, nx, ny))

        if len(connections) == 1:
            direction = next(iter(connections))
            symbols[(x, y)] = "│" if direction in ("N", "S") else "─"
        else:
            symbols[(x, y)] = PATH_CHARS.get(
                frozenset(connections), "•"
            )

    return symbols


def get_direction(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == -1:
        return "N"
    if dx == 1 and dy == 0:
        return "E"
    if dx == 0 and dy == 1:
        return "S"
    if dx == -1 and dy == 0:
        return "W"

    return ""


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{COLOR_RESET}"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_menu(
    generator: Any,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    path: list[str] | None = None,
) -> None:
    path_cells = path_to_cells(entry, path) if path else []
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

        if choice == "1" or choice.lower() == "m":
            grid = generator.generate(perfect)
            path = generator.solve(entry, exit_)
            path_cells = path_to_cells(entry, path) if path else []
        elif choice == "2" or choice.lower() == "p":
            show_path = not show_path
        elif choice == "3" or choice.lower() == "c":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4" or choice.lower() == "q":
            return
        else:
            error_message = "Invalid choice. Please select 1, 2, 3, or 4."
