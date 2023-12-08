from itertools import cycle
from math import lcm
from re import findall


class Map:
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            self.instructions = file.readline().rstrip()
            file.readline()
            self.graph = {}
            for line in file:
                node, left, right = findall(r"\w+", line)
                self.graph[node] = {"L": left, "R": right}

    def navigate(self, node: str) -> int:
        for i, instruction in enumerate(cycle(self.instructions)):
            if node.endswith("Z"):
                return i
            node = self.graph[node][instruction]
        assert False


def run(filename: str, hard: bool) -> int:
    map = Map(filename)
    if not hard:
        return map.navigate("AAA")
    return lcm(*(map.navigate(node) for node in map.graph if node.endswith("A")))
