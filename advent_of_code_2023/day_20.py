from collections import defaultdict, deque
from itertools import count
from math import lcm


class Module:
    def __init__(self) -> None:
        self.name = ""
        self.inputs = {}
        self.on = False
        self.type = ""
        self.outputs = []

    def process(self, source: str, sig: int) -> list[tuple[str, int, str]]:
        sig_out = None
        match self.type:
            case "b":
                sig_out = sig
            case "%" if not sig:
                self.on = not self.on
                sig_out = 1 if self.on else 0
            case "&":
                self.inputs[source] = sig
                sig_out = 0 if all(self.inputs.values()) else 1
        if sig_out is None:
            return []
        return [(self.name, sig_out, output) for output in self.outputs]


def run(filename: str, hard: bool) -> int:
    modules, to_watch = parse_modules(filename)
    queue = deque()
    count_low = 0
    count_high = 0
    cycles = []
    for step in count(1):
        queue.append(("", 0, "broadcaster"))
        while queue:
            source, sig, name = queue.popleft()
            if sig:
                count_high += 1
            else:
                count_low += 1
            queue.extend(modules[name].process(source, sig))
            if source in to_watch and sig:
                cycles.append(step)
                to_watch.remove(source)
        if hard and not to_watch:
            return lcm(*cycles)
        if not hard and step == 1000:
            return count_low * count_high
    assert False


def parse_modules(filename: str) -> tuple[dict[str, Module], set[str]]:
    modules = defaultdict(Module)
    last = None
    with open(filename) as file:
        for line in file:
            name, outputs = line.rstrip().split(" -> ")
            type = name[0]
            name = name.lstrip("&%")
            modules[name].name = name
            modules[name].type = type
            for output in outputs.split(", "):
                modules[name].outputs.append(output)
                modules[output].inputs[name] = 0
                if output == "rx":
                    assert type == "&"
                    last = name
    to_watch = set(modules[last].inputs.keys()) if last else set()
    return modules, to_watch
