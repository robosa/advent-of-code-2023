from collections import defaultdict
from collections.abc import Generator

COLORS_MAX = {"red": 12, "green": 13, "blue": 14}


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        if hard:
            return sum(get_min_power(line.rstrip()) for line in file)
        return sum(i + 1 for i, line in enumerate(file) if check_line(line.rstrip()))


def check_line(line: str) -> bool:
    return all(nb <= COLORS_MAX[color] for nb, color in parse_line(line))


def get_min_power(line: str) -> int:
    counts = defaultdict(int)
    for nb, color in parse_line(line):
        if nb > counts[color]:
            counts[color] = nb
    return counts["red"] * counts["green"] * counts["blue"]


def parse_line(line: str) -> Generator[tuple[int, str], None, None]:
    _, rounds = line.split(":")
    for round in rounds.split(";"):
        for count in round.split(","):
            nb, color = count[1:].split()
            yield int(nb), color
