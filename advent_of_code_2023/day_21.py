from collections import deque

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        grid = [line.rstrip() for line in file]
    n = len(grid)
    max_steps = 2 * n + n // 2
    part1 = 0
    full_grid = 0
    h_sect = [0, 0]
    queue = deque()
    queue.append((max_steps, max_steps, 0))
    seen = {(max_steps, max_steps)}
    while queue:
        i, j, step = queue.popleft()
        if step <= n // 2 and step % 2 == 0:
            part1 += 1
        if 2 * n < i <= 3 * n and 2 * n < j <= 3 * n:
            full_grid += 1
        if step % 2 == 1:
            h_sect[(j // n) % 2] += 1
        if step == max_steps:
            continue
        for di, dj in DIRECTIONS:
            ni, nj = i + di, j + dj
            if (ni, nj) not in seen and grid[ni % n][nj % n] != "#":
                seen.add((ni, nj))
                queue.append((ni, nj, step + 1))
    if not hard:
        return part1
    coeff = 26501365 // n - 1
    return h_sect[0] + coeff * (h_sect[1]) + (coeff * coeff - 1) * full_grid
