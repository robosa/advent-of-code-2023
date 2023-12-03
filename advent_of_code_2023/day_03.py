def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        input = [line.rstrip() for line in file]
    if hard:
        return part_two(input)
    return part_one(input)


def part_one(input: list[str]) -> int:
    res = 0
    for i, line in enumerate(input):
        is_num = False
        start = 0
        for j in range(len(line)):
            if not is_num and line[j].isdigit():
                start = j
                is_num = True
            elif is_num and not line[j].isdigit():
                if check_symbol(input, i, start, j):
                    res += int(line[start:j])
                is_num = False
        if is_num:
            if check_symbol(input, i, start, len(line)):
                res += int(line[start:])
    return res


def check_symbol(input: list[str], row: int, start: int, end: int) -> bool:
    return any(
        not (c.isdigit() or c == ".")
        for line in input[max(0, row - 1) : row + 2]
        for c in line[max(0, start - 1) : end + 1]
    )


def part_two(input: list[str]) -> int:
    return sum(
        get_gear_ratio(input, i, j)
        for i, line in enumerate(input)
        for j, char in enumerate(line)
        if char == "*"
    )


def get_gear_ratio(input: list[str], row: int, col: int) -> int:
    numbers = []
    for line in input[max(row - 1, 0) : row + 2]:
        numbers.extend(get_numbers_in_row(line, col))
    return numbers[0] * numbers[1] if len(numbers) == 2 else 0


def get_numbers_in_row(line: str, col: int) -> list[int]:
    if line[col].isdigit():
        return [get_number(line, col)]
    res = []
    if col > 0 and line[col - 1].isdigit():
        res.append(get_number(line, col - 1))
    if col < len(line) - 1 and line[col + 1].isdigit():
        res.append(get_number(line, col + 1))
    return res


def get_number(line: str, col: int) -> int:
    start = col
    end = col + 1
    while start > 0 and line[start - 1].isdigit():
        start -= 1
    while end < len(line) and line[end].isdigit():
        end += 1
    return int(line[start:end])
