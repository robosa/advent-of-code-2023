DIRECTIONS = {"L": (0, -1), "U": (-1, 0), "R": (0, 1), "D": (1, 0)}
SPLITTERS = {
    "-": {"L": ["L"], "U": ["L", "R"], "R": ["R"], "D": ["L", "R"]},
    "|": {"L": ["U", "D"], "U": ["U"], "R": ["U", "D"], "D": ["D"]},
}
MIRRORS = {
    "/": {"L": "D", "U": "R", "R": "U", "D": "L"},
    "\\": {"L": "U", "U": "L", "R": "D", "D": "R"},
}

Beam = tuple[int, int, str]


class Grid:
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            self.grid = file.read().split()
        self.n = len(self.grid)
        self.cache = {}

    def cast_beam(self, beam: Beam) -> int:
        beams = [beam]
        seen = set()
        energized = set()
        while beams:
            beam = beams.pop()
            if beam in seen:
                continue
            seen.add(beam)
            segment, splits = (
                self.cache[beam] if beam in self.cache else self.cast_segment(beam)
            )
            energized |= segment
            beams.extend(splits)
        return len(energized)

    def cast_segment(self, beam: Beam) -> tuple[set[tuple[int, int]], list[Beam]]:
        segment = set()
        splits = []
        i, j, d = beam
        while 0 <= i < self.n and 0 <= j < self.n:
            segment.add((i, j))
            tile = self.grid[i][j]
            if tile in "|-":
                for new_d in SPLITTERS[tile][d]:
                    di, dj = DIRECTIONS[new_d]
                    split = (i + di, j + dj, new_d)
                    splits.append(split)
                break
            if tile != ".":
                d = MIRRORS[tile][d]
            di, dj = DIRECTIONS[d]
            i, j = i + di, j + dj
        self.cache[beam] = segment, splits
        return segment, splits


def run(filename: str, hard: bool) -> int:
    grid = Grid(filename)
    if not hard:
        return grid.cast_beam((0, 0, "R"))
    n = grid.n
    return max(
        grid.cast_beam(beam)
        for i in range(n)
        for beam in ((i, n - 1, "L"), (n - 1, i, "U"), (i, 0, "R"), (0, i, "D"))
    )
