from collections.abc import Callable

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def run(filename: str, hard: bool) -> int:
    if hard:
        return decode(filename, find_first_hard, find_last_hard)
    return decode(filename, find_first_easy, find_last_easy)


def decode(
    filename: str, find_first: Callable[[str], int], find_last: Callable[[str], int]
) -> int:
    tens = 0
    units = 0
    with open(filename, "r") as file:
        for line in file:
            tens += find_first(line)
            units += find_last(line.rstrip())
    return tens * 10 + units


def find_first_easy(line: str) -> int:
    return next(int(c) for c in line if c.isdigit())


def find_last_easy(line: str) -> int:
    return next(int(c) for c in line[::-1] if c.isdigit())


def find_first_hard(line: str) -> int:
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])
        for j, digit in enumerate(DIGITS):
            if line[i:].startswith(digit):
                return j + 1
    raise ValueError("Not found")


def find_last_hard(line: str) -> int:
    for i in range(len(line), 0, -1):
        if line[i - 1].isdigit():
            return int(line[i - 1])
        for j, digit in enumerate(DIGITS):
            if line[:i].endswith(digit):
                return j + 1
    raise ValueError("Not found")
