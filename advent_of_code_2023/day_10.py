from itertools import count

DIRECTIONS = {"L": (0, -1), "U": (-1, 0), "R": (0, 1), "D": (1, 0)}
LEFT = {"L": (1, 0), "U": (0, -1), "R": (-1, 0), "D": (0, 1)}
RIGHT = {"L": (-1, 0), "U": (0, 1), "R": (1, 0), "D": (0, -1)}
TILES = {
    "-": {"L": "L", "R": "R"},
    "|": {"U": "U", "D": "D"},
    "L": {"D": "R", "L": "U"},
    "7": {"R": "D", "U": "L"},
    "J": {"R": "U", "D": "L"},
    "F": {"L": "D", "U": "R"},
}


class Grid:
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            self.grid = [list(line.rstrip()) for line in file]
        self.n = len(self.grid)
        self.m = len(self.grid[0])
        self.left_side = set()
        self.right_side = set()
        for i, row in enumerate(self.grid):
            if "S" in row:
                self.start = i, row.index("S")
                return
        assert False

    def is_in_grid(self, i: int, j: int) -> bool:
        return i >= 0 and i < self.n and j >= 0 and j < self.m

    def find_start_dir(self) -> str:
        i, j = self.start
        for direction, (di, dj) in DIRECTIONS.items():
            if self.is_in_grid(i + di, j + dj):
                tile = self.grid[i + di][j + dj]
                if tile != "." and direction in TILES[tile]:
                    return direction
        assert False

    def mark_loop(self) -> int:
        i, j = self.start
        direction = self.find_start_dir()
        for step in count(1):
            self.grid[i][j] = "X"
            self.store_sides(i, j, direction)
            di, dj = DIRECTIONS[direction]
            i, j = i + di, j + dj
            self.store_sides(i, j, direction)
            tile = self.grid[i][j]
            if tile == "X":
                return step
            direction = TILES[tile][direction]
        assert False

    def store_sides(self, i: int, j: int, direction: str) -> None:
        di, dj = LEFT[direction]
        if self.is_in_grid(i + di, j + dj):
            self.left_side.add((i + di, j + dj))
        di, dj = RIGHT[direction]
        if self.is_in_grid(i + di, j + dj):
            self.right_side.add((i + di, j + dj))

    def count_inside(self) -> int:
        for stack in (list(self.left_side), list(self.right_side)):
            count = 0
            is_inside = True
            while stack:
                i, j = stack.pop()
                if self.grid[i][j] in ("I", "X"):
                    continue
                if i == 0 or i == self.n - 1 or j == 0 or j == self.m - 1:
                    is_inside = False
                    break
                self.grid[i][j] = "I"
                count += 1
                for di, dj in DIRECTIONS.values():
                    ii, jj = i + di, j + dj
                    if self.is_in_grid(ii, jj) and self.grid[ii][jj] not in ("I", "X"):
                        stack.append((ii, jj))
            if is_inside:
                return count
        assert False


def run(filename: str, hard: bool) -> int:
    grid = Grid(filename)
    length = grid.mark_loop()
    return grid.count_inside() if hard else length // 2
