from config_parser import ConfigError

def write_maze_file(path: str, grid: list[list[int]],
                    entry: tuple[int, int], exit_: tuple[int, int],
                    solution: str) -> None:
    lines = []
    for row in grid:
        digits = []
        for cell in row:
            digits.append(format(cell, "X"))
        lines.append("".join(digits))
    lines.append("")
    lines.append(f"{entry[0]}, {entry[1]}")
    lines.append(f"{exit_[0]}, {exit_[1]}")
    lines.append(solution)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError as e:
        raise ConfigError(f"Cannot write '{path}': {e}")

# if __name__ == "__main__":
#     grid = [
#         [9, 3, 11],
#         [14, 12, 6],
#     ]
#     write_maze_file("test_maze.txt", grid, (0, 0), (2, 1), "ESE")