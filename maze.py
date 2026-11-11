import random
# for random.shuffle(numbers)
from collections import deque
# for BFS

N = 1
E = 2
S = 4
W = 8

OPPOSITE = {N: S, S: N, W: E, E: W}

DELTA = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}

pattern = [
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX"
]


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, a):
        # loop goes through the chain to the top, with a recursive thingy in while
        while self.parent[a] != a:
            a = self.parent[a]
        return a

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        # if they belong to the same group, no merge happened so it's false, even tho the group is the same
        if root_a == root_b:
            return False
        # union by size, if one group is bigger than the other,
        # its better to assign the parent of a bigger group to the whole union
        # because it's more efficient codewise for the find() method 
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        # the actual merge code lol
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]

        return True


class Mazegenerator:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        # creates a new instance of the Random class,
        # so if the seed is diff, the new shuffle thingy/instance will be created
        self.grid = [[15 for _ in range(width)]
            for _ in range(height)]
        # your own grid instance for this generator, this seed
        # 15 because at this point all the walls are closed compeltely
        self.blocked = set()
        # empty set, later i'll put 42 coordinates inside of it
        # it deletes walls in a cell then ajustes the cells around it

    def carve(self, x, y, d):
        dx, dy = DELTA[d]  # called "unpacking", it took values from DELTA[d] adn assigned them to dx, dy
        nx = x + dx
        ny = y + dy
        # it eliminates the d wall in the initial cell, and the OPPOSITE of the d wall in the other impacted cell
        self.grid[y][x] &= ~d
        self.grid[ny][nx] &= ~OPPOSITE[d]

    def _build_edges(self):
        edges = []
        for y in range(self.height):
            for x in range(self.width):
                # just to get the exact num of cells independently of the grid
                cell = y * self.width + x
                # 42 logo check
                if cell in self.blocked:
                    continue
                # Append E Neighbor
                if x + 1 < self.width:
                    neighbour = cell + 1
                    if neighbour not in self.blocked:
                        edges.append((cell, neighbour))
                # Append S Neighbor
                if y + 1 < self.height:
                    neighbour = cell + self.width
                    if neighbour not in self.blocked:
                        edges.append((cell, neighbour))
            # self.rng instead of just random.shuffle
            # because the shuffle depends on the seed of the generator, and it's cool
            self.rng.shuffle(edges)
        return edges

# it goes through every cell, testing the 3x3 area around
    def _has_open_3x3(self):
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                open_region = True
                # Check horizontal connections
                for dy in range(3):
                    for dx in range(2):
                        if self.grid[y + dy][x + dx] & E:
                            open_region = False
                # Check vertical connections
                for dy in range(2):
                    for dx in range(3):
                        if self.grid[y + dy][x + dx] & S:
                            open_region = False
                if open_region:
                    return True
        return False

    def _add_loops(self):
        edges = self._build_edges()
        for a, b in edges:
            x = a % self.width
            y = a // self.width
            if b == a + 1:
                direction = E
            else:
                direction = S
            # Skip walls already open
            if not (self.grid[y][x] & direction):
                continue
            # Random selection
            if self.rng.random() > 0.15:
                continue
            # Temporarily open the wall
            self.carve(x, y, direction)
            # Reject if it creates a fully open 3x3
            if self._has_open_3x3():
                self.grid[y][x] |= direction
                nx = b % self.width
                ny = b // self.width
                self.grid[ny][nx] |= OPPOSITE[direction]

    def generate(self, perfect=True):
        # Reset the grid -> so all walls are closed
        self.grid = [
            [15 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        # if it's a 3x3 grid = 9, good formula
        self.place_42_pattern()
        uf = UnionFind(self.width * self.height)
        edges = self._build_edges()
        for a, b in edges:
            # Convert cell ID into coordinates
            x = a % self.width
            # // it's integer division -> so decimal part is discarded
            # for example 10 // 3 = 3
            # for comparison: normal division: 10 / 3 = 3,333
            # it's to determine in which row is the cell 5// 3 still in the 1st
            y = a // self.width
            # if True remove E, if not the S
            # b is a valid neighbour because _build_edges() constructed the list
            if uf.union(a, b):
                if b == a + 1:
                    self.carve(x, y, E)
                else:
                    self.carve(x, y, S)
        if not perfect:
            self._add_loops()
        return self.grid

    def print_maze(self):
        # Print top border
        print("+" + "---+" * self.width)

        # Print vertical walls
        for y in range(self.height):
            row = "|"
            for x in range(self.width):
                cell = y * self.width + x
                if cell in self.blocked:
                    row += " X |"
                elif self.grid[y][x] & E:
                    row += "   |"
                else:
                    row += "    "
            print(row)
            # Print horizontal walls
            row = "+"
            for x in range(self.width):
                if self.grid[y][x] & S:
                    row += "---+"
                else:
                    row += "   +"
            print(row)

    def place_42_pattern(self):
        self.blocked.clear()

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        offset_x = (self.width - pattern_width) // 2
        offset_y = (self.height - pattern_height) // 2

        if offset_x < 0 or offset_y < 0:
            print("Maze too small for the 42 pattern")
            return

        for pattern_y, row in enumerate(pattern):
            for pattern_x, char in enumerate(row):
                if char == "X":
                    maze_x = offset_x + pattern_x
                    maze_y = offset_y + pattern_y
                    cell = maze_y * self.width + maze_x
                    self.blocked.add(cell)

    def solve(self, entry, exit_):
        queue = deque([entry])
        visited = {entry}
        parent = {}
        directions = {
            N: "N",
            E: "E",
            S: "S",
            W: "W"
        }
        while queue:
            current = queue.popleft()
            x, y = current
            if current == exit_:
                break
            for direction, (dx, dy) in DELTA.items():
                # Check if the wall is closed
                if self.grid[y][x] & direction:
                    continue
                nx = x + dx
                ny = y + dy
                neighbour = (nx, ny)
                # Check maze boundaries
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                # Avoid visiting the same cell twice
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                parent[neighbour] = (current, directions[direction])
                queue.append(neighbour)
        # Check whether the exit was reached
        if exit_ not in visited:
            return None
        # Reconstruct the path backwards
        path = []
        current = exit_
        while current != entry:
            previous, direction = parent[current]
            path.append(direction)
            current = previous
        path.reverse()
        return path

# Test the maze generator
# maze = Mazegenerator(20, 30, seed=42)
# grid = maze.generate()
# for row in grid:
#     print(row)

# # Test the randomness of the generator
# maze1 = Mazegenerator(4, 4, seed=42)
# maze2 = Mazegenerator(4, 4, seed=42)
# print(maze1.generate() == maze2.generate())

# # Test that every edge appears only once
# maze = Mazegenerator(3, 3, seed=42)
# edges = maze._build_edges()
# print(edges)
# print("Total edges:", len(edges))
# print("Unique edges:", len(set(edges)))
# # Test Seeds
# maze1 = Mazegenerator(3, 3, seed=123)
# maze2 = Mazegenerator(3, 3, seed=123)
# edges1 = maze1._build_edges()
# edges2 = maze2._build_edges()
# print(edges1 == edges2)  # Usually False

# in the end u have a list with all possible connections = edges
# maze1 = Mazegenerator(4, 3, seed=42)
# maze2 = Mazegenerator(6,6, seed=12323)

# print(maze1.width)
# print(maze1.height)
# print(maze1.grid)
# print(maze1.blocked)
# print(maze2.grid)

# Y axis inversé, X reste le même

#test remouving a wall
# cell = 15
# print(bin(cell))
# cell &= ~E
# print(cell)
# print(bin(cell))

# & is used to check if the cell exists
# if cell & E:
#     print("East wall exists")
# if cell & W:
#     print("West wall exists")
# if cell & S:
#     print("South wall exists")
# if cell & N:
#     print("North wall exists")

# | is useful if you wann add a wall to a cell = OR

# ~ NOT operator, it can be used to substract a wall from a cell
# like 15 & ~2 = 13

# test the carve
# maze = Mazegenerator(3, 3)
# maze.carve(1, 1, N)
# maze.carve(1, 1, E)
# maze.carve(1, 1, S)
# maze.carve(1, 1, W)
# for row in maze.grid:
#     print(row)

# test the find method
# uf = UnionFind(6)
# uf.parent[1] = 0
# uf.parent[2] = 0
# print(uf.parent)
# print(uf.size)
# for i in range(6):
#     print(uf.find(i))

# test the union method
# uf = UnionFind(6)
# print(uf.union(0, 1))  # True
# print(uf.union(1, 2))  # True
# print(uf.union(0, 2))  # False
# print(uf.parent)
# print(uf.size)

# 0 --- 1
# |     |
# 2 --- 3
# only 4 possible connections
# edges = [
#     (0, 1),  # 0 to 1, East
#     (0, 2),  # 0 to 2, South
#     (1, 3),  # 1 to 3, South
#     (2, 3)   # 2 to 3, East
# ]

#Test the build the edges function
# maze = Mazegenerator(2, 2)
# edges = maze._build_edges()
# print("Test 1:", edges)
# maze = Mazegenerator(2, 2)
# maze.blocked.add(1)
# edges = maze._build_edges()
# print("Test 2:", edges)
# maze = Mazegenerator(1, 1)
# edges = maze._build_edges()
# print("Test 3:", edges)
# Test 1: 2x2 grid
# Expected: [(0, 1), (0, 2), (1, 3), (2, 3)]
# Test 2: 2x2 grid with cell 1 blocked
# Expected: [(0, 2), (2, 3)]
# Test 3: 1x1 grid
# Expected: []

## Test WALL:
# def test_maze(maze):
#     grid = maze.grid
#     width = maze.width
#     height = maze.height

#     open_cells = [
#         y * width + x
#         for y in range(height)
#         for x in range(width)
#         if y * width + x not in maze.blocked
#     ]

#     # 1. Count open internal walls
#     open_edges = 0

#     for y in range(height):
#         for x in range(width):
#             cell = grid[y][x]

#             if x < width - 1 and not (cell & E):
#                 open_edges += 1

#             if y < height - 1 and not (cell & S):
#                 open_edges += 1

#     assert open_edges == len(open_cells) - 1

#     # 2. Check outer walls
#     for x in range(width):
#         assert grid[0][x] & N
#         assert grid[height - 1][x] & S

#     for y in range(height):
#         assert grid[y][0] & W
#         assert grid[y][width - 1] & E

#     # 3. Check blocked cells
#     for cell in maze.blocked:
#         x = cell % width
#         y = cell // width
#         assert grid[y][x] == 15

#     print("Maze checks passed!")


# maze = Mazegenerator(4, 4, seed=42)
# maze.generate()
# test_maze(maze)

# test maze print
# maze = Mazegenerator(3, 3, seed=43)
# maze.generate()
# maze.print_maze()

maze = Mazegenerator(30, 30, seed=43)
maze.generate()
maze.print_maze()


# maze = Mazegenerator(15, 15)
# maze.place_42_pattern()
# for y in range(maze.height):
#     for x in range(maze.width):
#         cell = y * maze.width + x
#         if cell in maze.blocked:
#             print("X", end=" ")
#         else:
#             print(".", end=" ")
#     print()
# # print("Blocked cells:", len(maze.blocked))
# # print("Blocked IDs:", sorted(maze.blocked))
# maze.print_maze()

# maze.generate()
# print("Blocked cells:", len(maze.blocked))
# maze.print_maze()
