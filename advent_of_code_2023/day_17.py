from heapq import heappop, heappush

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def run(filename: str, hard: bool) -> int:
    with open(filename) as file:
        grid = [list(map(int, line.rstrip())) for line in file]
    n = len(grid)
    goal = (n - 1, n - 1)
    min_streak, max_streak = (4, 10) if hard else (1, 3)
    queue = []
    heappush(queue, (0, 0, 0, 0, 0))
    heappush(queue, (0, 0, 0, 1, 0))
    seen = {(0, 0, 0), (0, 0, 1)}
    while queue:
        cost, i, j, d, streak = heappop(queue)
        di, dj = DIRECTIONS[d]
        i, j = i + di, j + dj
        if not (0 <= i < n and 0 <= j < n):
            continue
        cost += grid[i][j]
        streak += 1
        if streak >= min_streak and (i, j) == goal:
            return cost
        if streak < max_streak:
            heappush(queue, (cost, i, j, d, streak))
            if streak < min_streak:
                continue
        if (i, j, d % 2) not in seen:
            seen.add((i, j, d % 2))
            heappush(queue, (cost, i, j, (d + 1) % 4, 0))
            heappush(queue, (cost, i, j, (d + 3) % 4, 0))
    assert False
