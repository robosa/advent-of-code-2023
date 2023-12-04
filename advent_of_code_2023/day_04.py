def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        matches = [count_matches(line) for line in file]
    if not hard:
        return sum(1 << (m - 1) for m in matches if m)
    n = len(matches)
    cards = [1] * n
    res = 0
    for i, (c, m) in enumerate(zip(cards, matches)):
        res += c
        for j in range(i + 1, min(i + m + 1, n)):
            cards[j] += c
    return res


def count_matches(line: str) -> int:
    winning, actual = line.split(":")[1].split("|")
    return len(set(winning.split()).intersection(actual.split()))
