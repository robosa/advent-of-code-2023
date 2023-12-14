from itertools import count


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        grid = [list(row) for row in file.read().split()]
    n = len(grid)
    return part_two(grid, n) if hard else part_one(grid, n)


def part_one(grid: list[list[str]], n: int) -> int:
    res = 0
    for j in range(n):
        weight = n
        for i in range(n):
            match grid[i][j]:
                case "O":
                    res += weight
                    weight -= 1
                case "#":
                    weight = n - i - 1
    return res


def part_two(grid: list[list[str]], n: int) -> int:
    cache = {}
    for step in count():
        for _ in range(4):
            grid = tilt_and_rotate(grid, n)
        grid_str = "\n".join(["".join(row) for row in grid])
        if grid_str not in cache:
            cache[grid_str] = step
            continue
        start = cache[grid_str]
        end = start + (999999999 - step) % (step - start)
        final = next(s.split("\n") for s, i in cache.items() if i == end)
        return sum(row.count("O") * (n - i) for i, row in enumerate(final))
    assert False


def tilt_and_rotate(grid: list[list[str]], n: int) -> list[list[str]]:
    new_grid = [["."] * n for _ in range(n)]
    for j, new_row in enumerate(new_grid):
        next_pos = n
        for i in range(n):
            match grid[i][j]:
                case "O":
                    next_pos -= 1
                    new_row[next_pos] = "O"
                case "#":
                    next_pos = n - i - 1
                    new_row[next_pos] = "#"
    return new_grid
