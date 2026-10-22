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

def render_maze(self, maze: list[list[int]]) -> None:
    """Render a maze using ASCII characters."""
    north = 1
    east = 2
    south = 4
    west = 8

    height = len(maze)
    width = len(maze[0])

    for y in range(height):
        top_line = "+"
        cell_line = ""

        for x in range(width):
            cell = maze[y][x]

            if cell & north:
                top_line += "---+"
            else:
                top_line += "   +"

            if cell & west:
                cell_line += "|"
            else:
                cell_line += " "

            cell_line += "   "

        cell_line += "|" if maze[y][width - 1] & east else " "
        print(top_line)
        print(cell_line)

    bottom_line = "+"
    for x in range(width):
        cell = maze[height - 1][x]

        if cell & south:
            bottom_line += "---+"
        else:
            bottom_line += "   +"

    print(bottom_line)
