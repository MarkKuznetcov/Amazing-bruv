"""Terminal (ASCII + ANSI colours) display for the maze.

Wall bits (agreed format): N=1, E=2, S=4, W=8, grid stored as grid[y][x].
A cell equal to 15 (all four walls closed) is part of the "42" pattern.
"""

import os
import sys
from typing import Callable

os.system("")  # enables ANSI colours in older Windows consoles

N, E, S, W = 1, 2, 4, 8
DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

RESET = "\033[0m"

# (name, ANSI 256-colour code)
WALL_COLORS = [("white", 255), ("blue", 27), ("magenta", 127),
               ("cyan", 37), ("grey", 244)]
PATTERN_COLORS = [("orange", 208), ("pink", 213), ("lime", 118),
                  ("white", 255), ("red", 160)]
ENTRY_BG = 34
EXIT_BG = 160
PATH_BG = 220

Grid = list[list[int]]
Regenerate = Callable[[], tuple[Grid, str]]

MENU = (
    "\n[1] Re-generate a new maze\n"
    "[2] Show / hide the shortest path\n"
    "[3] Change wall colour\n"
    "[4] Change '42' colour\n"
    "[5] Quit\n"
)


def _paint(bg: int, text: str = "  ") -> str:
    return f"\033[30;48;5;{bg}m{text}{RESET}"


class MazeDisplay:
    """Draws a maze in the terminal and runs an interactive menu."""

    def __init__(self, grid: Grid, entry: tuple[int, int],
                 exit_: tuple[int, int], solution: str,
                 regenerate: Regenerate) -> None:
        self.entry = entry
        self.exit = exit_
        self.regenerate = regenerate
        self.show_path = True
        self.wall_idx = 0
        self.pattern_idx = 0
        self.set_maze(grid, solution)

    def set_maze(self, grid: Grid, solution: str) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.solution = solution
        self.path_tiles = self._compute_path_tiles()

    # ---------- geometry ----------
    # The maze is drawn on a (2W+1) x (2H+1) grid of tiles:
    # odd/odd = cell, even/even = pillar, mixed = wall or passage.

    def _compute_path_tiles(self) -> set[tuple[int, int]]:
        tx, ty = 2 * self.entry[0] + 1, 2 * self.entry[1] + 1
        tiles = {(tx, ty)}
        for letter in self.solution:
            if letter not in DIRS:
                continue
            dx, dy = DIRS[letter]
            tiles.add((tx + dx, ty + dy))
            tx, ty = tx + 2 * dx, ty + 2 * dy
            tiles.add((tx, ty))
        return tiles

    def _is_wall(self, tx: int, ty: int) -> bool:
        if tx % 2 == 0 and ty % 2 == 0:
            return True
        if tx % 2 == 1 and ty % 2 == 1:
            return False
        if tx % 2 == 0:  # vertical wall between two cells of row y
            y = (ty - 1) // 2
            if tx == 0:
                return bool(self.grid[y][0] & W)
            return bool(self.grid[y][tx // 2 - 1] & E)
        x = (tx - 1) // 2  # horizontal wall between two cells of column x
        if ty == 0:
            return bool(self.grid[0][x] & N)
        return bool(self.grid[ty // 2 - 1][x] & S)

    # ---------- rendering ----------

    def _tile(self, tx: int, ty: int) -> str:
        if self._is_wall(tx, ty):
            return _paint(WALL_COLORS[self.wall_idx][1])
        if tx % 2 == 1 and ty % 2 == 1:
            cell = (tx // 2, ty // 2)
            if cell == self.entry:
                return _paint(ENTRY_BG, "IN")
            if cell == self.exit:
                return _paint(EXIT_BG, "EX")
            if self.grid[cell[1]][cell[0]] == 15:
                return _paint(PATTERN_COLORS[self.pattern_idx][1])
        if self.show_path and (tx, ty) in self.path_tiles:
            return _paint(PATH_BG)
        return "  "

    def render(self) -> str:
        rows = []
        for ty in range(2 * self.height + 1):
            rows.append("".join(self._tile(tx, ty)
                                for tx in range(2 * self.width + 1)))
        return "\n".join(rows)

    # ---------- interaction ----------

    @staticmethod
    def _clear() -> None:
        if sys.stdout.isatty():
            print("\033[H\033[2J", end="")

    def run(self) -> None:
        message = ""
        while True:
            self._clear()
            print(self.render())
            print(MENU)
            if message:
                print(message)
            try:
                choice = input("Your choice: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            message = self._handle(choice)
            if message == "quit":
                return

    def _handle(self, choice: str) -> str:
        if choice == "1":
            try:
                grid, solution = self.regenerate()
            except Exception as e:  # keep the menu alive
                return f"Could not generate a new maze: {e}"
            self.set_maze(grid, solution)
            return "New maze generated."
        if choice == "2":
            self.show_path = not self.show_path
            return "Path shown." if self.show_path else "Path hidden."
        if choice == "3":
            self.wall_idx = (self.wall_idx + 1) % len(WALL_COLORS)
            return f"Wall colour: {WALL_COLORS[self.wall_idx][0]}"
        if choice == "4":
            self.pattern_idx = (self.pattern_idx + 1) % len(PATTERN_COLORS)
            return f"'42' colour: {PATTERN_COLORS[self.pattern_idx][0]}"
        if choice == "5":
            return "quit"
        return f"Unknown choice '{choice}', pick 1-5."