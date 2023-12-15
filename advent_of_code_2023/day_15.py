class Box:
    def __init__(self) -> None:
        self.lenses = []

    def remove(self, label: str) -> None:
        for i, (s, _) in enumerate(self.lenses):
            if s == label:
                self.lenses.pop(i)
                return

    def add(self, label: str, power: str) -> None:
        for i, (s, _) in enumerate(self.lenses):
            if s == label:
                self.lenses[i] = (s, power)
                return
        self.lenses.append((label, power))

    def score(self) -> int:
        return sum((i + 1) * int(p) for i, (_, p) in enumerate(self.lenses))


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        sequence = file.readline().rstrip().split(",")
    if not hard:
        return sum(map(hash, sequence))
    boxes = [Box() for _ in range(256)]
    for instruction in sequence:
        if instruction.endswith("-"):
            label = instruction[:-1]
            boxes[hash(label)].remove(label)
        else:
            label, power = instruction.split("=")
            boxes[hash(label)].add(label, power)
    return sum(box.score() * (i + 1) for i, box in enumerate(boxes))


def hash(label: str) -> int:
    res = 0
    for c in label:
        res = ((res + ord(c)) * 17) % 256
    return res
