from copy import copy
from math import prod
from operator import gt, lt
from re import compile
from typing import Optional

Ratings = dict[str, tuple[int, int]]

CATEGORY_RANGES: Ratings = {
    "x": (1, 4000),
    "m": (1, 4000),
    "a": (1, 4000),
    "s": (1, 4000),
}


class Rule:
    def __init__(self, input: str) -> None:
        condition, self.dest = input.split(":")
        self.category = condition[0]
        self.op = lt if condition[1] == "<" else gt
        self.value = int(condition[2:])

    def apply_part(self, part: dict[str, int]) -> Optional[str]:
        return self.dest if self.op(part[self.category], self.value) else None

    def apply_ratings(
        self, ratings: Ratings
    ) -> tuple[str, Optional[Ratings], Optional[Ratings]]:
        a, b = ratings[self.category]
        ok, nok = None, None
        match (self.op(a, self.value), self.op(b, self.value)):
            case True, True:
                ok = (a, b)
            case False, False:
                nok = (a, b)
            case True, _:
                ok = (a, self.value - 1)
                nok = (self.value, b)
            case _:
                nok = (a, self.value)
                ok = (self.value + 1, b)
        ratings_ok = None
        ratings_nok = None
        if ok is not None:
            ratings_ok = copy(ratings)
            ratings_ok[self.category] = ok
        if nok is not None:
            ratings_nok = copy(ratings)
            ratings_nok[self.category] = nok
        return self.dest, ratings_ok, ratings_nok


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        input, parts = file.read().split("\n\n")
    workflows = parse_workflows(input.split())
    return part_two(workflows) if hard else part_one(workflows, parts)


def part_one(workflows: dict[str, tuple[list[Rule], str]], parts: str) -> int:
    res = 0
    pattern = compile(r"(\w)=(\d+)")
    for part_str in parts.split():
        part = {k: int(v) for k, v in pattern.findall(part_str)}
        name = "in"
        while name not in ("A", "R"):
            rules, default = workflows[name]
            for rule in rules:
                name = rule.apply_part(part)
                if name is not None:
                    break
            if name is None:
                name = default
        if name == "A":
            res += sum(part.values())
    return res


def part_two(workflows: dict[str, tuple[list[Rule], str]]) -> int:
    valid = []
    queue: list[tuple[str, Ratings]] = [("in", CATEGORY_RANGES)]
    ok, nok = None, None
    while queue:
        name, ratings = queue.pop()
        rules, default = workflows[name]
        for rule in rules:
            dest, ok, nok = rule.apply_ratings(ratings)
            if ok is not None:
                if dest == "A":
                    valid.append(ok)
                elif dest != "R":
                    queue.append((dest, ok))
            if nok is None:
                break
            ratings = nok
        if nok is not None:
            if default == "A":
                valid.append(nok)
            elif default != "R":
                queue.append((default, nok))
    return sum(prod(b - a + 1 for a, b in part.values()) for part in valid)


def parse_workflows(inputs: list[str]) -> dict[str, tuple[list[Rule], str]]:
    workflows = {}
    for workflow in inputs:
        name, rules_str = workflow[:-1].split("{")
        rules = rules_str.split(",")
        workflows[name] = [Rule(rule) for rule in rules[:-1]], rules[-1]
    return workflows
