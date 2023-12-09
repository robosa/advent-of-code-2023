from itertools import pairwise


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        return sum(predict(line, hard) for line in file)


def predict(line: str, hard: bool) -> int:
    seq = [int(i) for i in line.split()[:: -1 if hard else 1]]
    res = 0
    while any(seq):
        res += seq[-1]
        seq = [b - a for a, b in pairwise(seq)]
    return res
