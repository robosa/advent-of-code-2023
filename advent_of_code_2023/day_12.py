from re import compile, sub


class RowCounter:
    def __init__(self, line: str, hard: bool) -> None:
        row, blocks = line.split()
        self.blocks = list(map(int, blocks.split(",")))
        if hard:
            row = "?".join([row] * 5)
            self.blocks = self.blocks * 5
        self.row = sub(r"\.+", ".", row.lstrip(".") + ".")
        self.patterns = [compile(rf"[\?#]{{{b}}}[\?\.]") for b in self.blocks]
        self.cache = {}

    def count(self, i: int, b: int) -> int:
        if (i, b) in self.cache:
            return self.cache[(i, b)]
        if b == len(self.blocks):
            self.cache[(i, b)] = 1 if "#" not in self.row[i:] else 0
            return self.cache[(i, b)]
        if i > len(self.row) - sum(self.blocks[b:]) - len(self.blocks[b:]):
            self.cache[(i, b)] = 0
            return 0
        res = self.count(i + 1, b) if self.row[i] != "#" else 0
        if self.patterns[b].match(self.row[i:]):
            res += self.count(i + self.blocks[b] + 1, b + 1)
        self.cache[(i, b)] = res
        return res


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        return sum(RowCounter(line, hard).count(0, 0) for line in file)
