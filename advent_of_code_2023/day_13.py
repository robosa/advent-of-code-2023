def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        grids = [block.split() for block in file.read().split("\n\n")]
    hundreds = 0
    units = 0
    for grid in grids:
        res = find_mirror(grid, hard)
        if res:
            hundreds += res
        else:
            units += find_mirror(list(map("".join, zip(*grid))), hard)
    return hundreds * 100 + units


def find_mirror(grid: list[str], hard: bool) -> int:
    diff = 0
    for i in range(len(grid) - 1):
        ok = not hard
        for j in range(min(i + 1, len(grid) - i - 1)):
            if grid[i - j] != grid[i + j + 1]:
                ok = not ok
                if not ok:
                    break
                diff = j
        if ok and (not hard or is_valid(grid[i - diff], grid[i + diff + 1])):
            return i + 1
    return 0


def is_valid(row1: str, row2: str) -> bool:
    return sum(c1 != c2 for c1, c2 in zip(row1, row2)) == 1
