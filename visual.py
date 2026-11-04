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

BLOCKED_CELL = "█"
# maybe I should add the walls etc like that?

def render_maze(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]],
    blocked: set[int],
) -> None:
    north = 1
    east = 2
    south = 4
    west = 8

    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        top_line = "+"
        cell_line = ""

        for x in range(width):
            cell = grid[y][x]
            cell_id = y * width + x

            if cell & north:
                top_line += "---+"
            else:
                top_line += "   +"

            if cell & west:
                cell_line += "|"
            else:
                cell_line += " "

            # Add the cell content
            if cell_id in blocked:
                cell_line += BLOCKED_CELL * 3
            elif (x, y) == entry:
                cell_line += " S "
            elif (x, y) == exit_:
                cell_line += " E "
            elif (x, y) in path:
                cell_line += " . "
            else:
                cell_line += "   "

        cell_line += "|" if grid[y][width - 1] & east else " "
        print(top_line)
        print(cell_line)

    bottom_line = "+"
    for x in range(width):
        cell = grid[height - 1][x]

        if cell & south:
            bottom_line += "---+"
        else:
            bottom_line += "   +"

    print(bottom_line)


def path_to_cells():
    """Convert the shortest path into coordinates."""
    pass


def colorize():
    """Apply an ANSI color to text."""
    pass


def display_menu():
    """Handle user interactions."""
    # 1. Regenerate maze
    # 2. Show/hide shortest path
    # 3. Change wall color
    # 4. Quit
    pass
