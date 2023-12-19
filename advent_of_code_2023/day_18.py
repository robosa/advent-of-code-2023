from itertools import pairwise

DIRECTIONS = {"R": 0, "D": 1, "L": 2, "U": 3}
DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Grid:
    def __init__(self, instructions: list[tuple[int, int]]) -> None:
        self.instructions = instructions
        self.digged = set()
        self.inside = set()
        self._set_grid_dims()

    def _set_grid_dims(self) -> None:
        i, j = 0, 0
        i_set = set()
        j_set = set()
        for d, dist in self.instructions:
            di, dj = DELTAS[d]
            i, j = i + dist * di, j + dist * dj
            i_set.add(i)
            j_set.add(j)
        start_i, start_j = 0, 0
        self.heights = [1]
        for i1, i2 in pairwise(sorted(i_set)):
            self.heights.append(i2 - i1 - 1)
            self.heights.append(1)
            if i2 == 0:
                start_i = len(self.heights) - 1
        self.widths = [1]
        for j1, j2 in pairwise(sorted(j_set)):
            self.widths.append(j2 - j1 - 1)
            self.widths.append(1)
            if j2 == 0:
                start_j = len(self.widths) - 1
        self.start = (start_i, start_j)

    def dig_loop(self) -> None:
        i, j = self.start
        self.digged = {self.start}
        left_side = set()
        right_side = set()
        for d, dist in self.instructions:
            di, dj = DELTAS[d]
            side_di, side_dj = DELTAS[(d + 1) % 4]
            left_side.add((i - side_di, j - side_dj))
            right_side.add((i + side_di, j + side_dj))
            while dist > 0:
                i, j = i + di, j + dj
                dist -= abs(di * self.heights[i]) + abs(dj * self.widths[j])
                self.digged.add((i, j))
                left_side.add((i - side_di, j - side_dj))
                right_side.add((i + side_di, j + side_dj))
        self.inside = right_side if min(left_side) < min(self.digged) else left_side

    def get_area(self) -> int:
        digged = self.inside | self.digged
        queue = list(self.inside - self.digged)
        while queue:
            i, j = queue.pop()
            for di, dj in DELTAS:
                np = (i + di, j + dj)
                if np not in digged:
                    queue.append(np)
                    digged.add(np)
        return sum(self.heights[i] * self.widths[j] for (i, j) in digged)


def run(filename: str, hard: bool) -> int:
    grid = Grid(get_instructions(filename, hard))
    grid.dig_loop()
    return grid.get_area()


def get_instructions(filename: str, hard: bool) -> list[tuple[int, int]]:
    instructions = []
    with open(filename) as file:
        for line in file:
            d, dist, hexa = line.split()
            if hard:
                instructions.append((int(hexa[7]), int(hexa[2:7], 16)))
            else:
                instructions.append((DIRECTIONS[d], int(dist)))
    return instructions
