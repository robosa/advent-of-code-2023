from collections import defaultdict
from itertools import combinations
from re import finditer


def run(filename: str, hard: bool) -> int:
    increase = 999999 if hard else 1
    cols = defaultdict(list)
    offset = 0
    with open(filename, "r") as file:
        for row, line in enumerate(file):
            if "#" not in line:
                offset += increase
                continue
            for galaxy in finditer("#", line):
                cols[galaxy.start()].append(row + offset)
    galaxies = []
    offset = 0
    for col in range(max(cols) + 1):
        if col in cols:
            galaxies.extend((row, col + offset) for row in cols[col])
        else:
            offset += increase
    return sum(abs(a - b) for p in combinations(galaxies, 2) for a, b in zip(*p))
