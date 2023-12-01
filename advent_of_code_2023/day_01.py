DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def run(filename: str, hard: bool = False) -> int:
    with open(filename, "r") as file:
        decs = 0
        units = 0
        for line in file:
            decs += find_first(line, hard)
            units += find_last(line, hard)
    return decs * 10 + units


def find_first(line: str, hard: bool) -> int:
    for i in range(len(line)):
        if line[i].isdigit():
            return int(line[i])
        if not hard:
            continue
        for j, digit in enumerate(DIGITS):
            if line[i:].startswith(digit):
                return j + 1
    raise ValueError("Not found")


def find_last(line: str, hard: bool) -> int:
    for i in range(len(line), 0, -1):
        if line[i - 1].isdigit():
            return int(line[i - 1])
        if not hard:
            continue
        for j, digit in enumerate(DIGITS):
            if line[:i].endswith(digit):
                return j + 1
    raise ValueError("Not found")
