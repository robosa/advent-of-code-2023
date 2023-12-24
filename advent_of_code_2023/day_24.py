from __future__ import annotations

from itertools import combinations

import numpy as np

MIN_TEST = 200000000000000
MAX_TEST = 400000000000000


class Hailstone:
    def __init__(self, input: str) -> None:
        p, v = input.rstrip().split("@")
        self.x, self.y, self.z = tuple(map(int, p.split(",")))
        self.vx, self.vy, self.vz = tuple(map(int, v.split(",")))

    def intersect_with(self, other: Hailstone) -> bool:
        d = self.vx * other.vy - self.vy * other.vx
        if not d:
            return False
        dx, dy = other.x - self.x, other.y - self.y
        t_self = (dx * other.vy - dy * other.vx) / d
        t_other = (dx * self.vy - dy * self.vx) / d
        return (
            (t_self > 0 and t_other > 0)
            and MIN_TEST <= self.x + t_self * self.vx <= MAX_TEST
            and MIN_TEST <= self.y + t_self * self.vy <= MAX_TEST
        )


def run(filename: str, hard: bool) -> int:
    with open(filename, "r") as file:
        hailstones = [Hailstone(line) for line in file]
    if not hard:
        return sum(h0.intersect_with(h1) for h0, h1 in combinations(hailstones, 2))
    h0, h1, h2 = hailstones[:3]
    a = np.array(
        [
            [0, h1.vz - h0.vz, h0.vy - h1.vy, 0, h1.z - h0.z, h0.y - h1.y],
            [h0.vz - h1.vz, 0, h1.vx - h0.vx, h0.z - h1.z, 0, h1.x - h0.x],
            [h1.vy - h0.vy, h0.vx - h1.vx, 0, h1.y - h0.y, h0.x - h1.x, 0],
            [0, h2.vz - h0.vz, h0.vy - h2.vy, 0, h2.z - h0.z, h0.y - h2.y],
            [h0.vz - h2.vz, 0, h2.vx - h0.vx, h0.z - h2.z, 0, h2.x - h0.x],
            [h2.vy - h0.vy, h0.vx - h2.vx, 0, h2.y - h0.y, h0.x - h2.x, 0],
        ]
    )
    b = np.array(
        [
            h1.y * h1.vz - h1.z * h1.vy - h0.y * h0.vz + h0.z * h0.vy,
            h1.z * h1.vx - h1.x * h1.vz - h0.z * h0.vx + h0.x * h0.vz,
            h1.x * h1.vy - h1.y * h1.vx - h0.x * h0.vy + h0.y * h0.vx,
            h2.y * h2.vz - h2.z * h2.vy - h0.y * h0.vz + h0.z * h0.vy,
            h2.z * h2.vx - h2.x * h2.vz - h0.z * h0.vx + h0.x * h0.vz,
            h2.x * h2.vy - h2.y * h2.vx - h0.x * h0.vy + h0.y * h0.vx,
        ]
    )
    return int(sum(np.linalg.solve(a, b)[:3]))
