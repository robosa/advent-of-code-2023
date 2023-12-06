from math import ceil, prod, sqrt


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        times = file.readline().split(":")[1].split()
        dists = file.readline().split(":")[1].split()
    if hard:
        return solve_race(int("".join(times)), int("".join(dists)))
    return prod(solve_race(int(time), int(dist)) for time, dist in zip(times, dists))


def solve_race(time: int, dist: int) -> int:
    root = ceil((time - sqrt(time * time - 4 * dist)) / 2)
    if (time - root) * root == dist:
        root += 1
    return time - 2 * root + 1
