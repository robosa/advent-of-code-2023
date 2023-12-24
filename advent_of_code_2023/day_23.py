from collections import defaultdict

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
SLOPES = [">", "v", "<", "^"]


class Grid:
    def __init__(self, filename: str) -> None:
        with open(filename) as file:
            self.grid = [line.rstrip() for line in file]
        n = len(self.grid)
        self.end = (n - 1, n - 2)
        self.graph = defaultdict(set)

    def walk_segment(self, i: int, j: int, dir: int) -> tuple[int, int, int]:
        di, dj = DIRECTIONS[dir]
        i, j = i + di, j + dj
        tile = self.grid[i][j]
        steps = 1
        while tile == "." and (i, j) != self.end:
            for ndir, (di, dj) in enumerate(DIRECTIONS):
                if ndir == (dir + 2) % 4:
                    continue
                ni, nj = i + di, j + dj
                tile = self.grid[ni][nj]
                if tile != "#":
                    i, j = ni, nj
                    dir = ndir
                    break
            steps += 1
        if (i, j) == self.end:
            return i, j, steps
        return i + di, j + dj, steps + 2

    def build_graph(self) -> int:
        res = 0
        queue = []
        si, sj, sdist = self.walk_segment(0, 1, 1)
        self.graph[(0, 1)].add(((si, sj), sdist))
        queue.append((si, sj, sdist))
        while queue:
            i, j, dist = queue.pop()
            if (i, j) == self.end:
                if dist > res:
                    res = dist
                continue
            for ndir, (di, dj) in enumerate(DIRECTIONS):
                ni, nj = i + di, j + dj
                if self.grid[ni][nj] == SLOPES[ndir]:
                    si, sj, sdist = self.walk_segment(ni, nj, ndir)
                    self.graph[(i, j)].add(((si, sj), sdist))
                    if (si, sj) != self.end:
                        self.graph[(si, sj)].add(((i, j), sdist))
                    queue.append((si, sj, dist + sdist))
        return res

    def find_longest(self, p: tuple[int, int], pred: set[tuple[int, int]]) -> int:
        for np, dist in self.graph[p]:
            if np == self.end:
                return dist
        res = 0
        for np, dist in self.graph[p]:
            if np not in pred:
                pred.add(np)
                dist += self.find_longest(np, pred)
                if dist > res:
                    res = dist
                pred.remove(np)
        return res


def run(filename: str, hard: bool) -> int:
    grid = Grid(filename)
    part1 = grid.build_graph()
    if not hard:
        return part1
    return grid.find_longest((0, 1), set())
