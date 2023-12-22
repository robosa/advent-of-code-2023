from collections import defaultdict


def run(filename: str, hard: bool) -> int:
    n, supported_by, supporting = stack_bricks(filename)
    if not hard:
        unsafe = set()
        for support in supported_by.values():
            if len(support) == 1:
                unsafe |= support
        return n - len(unsafe)
    falling = 0
    for disintegrated in supporting:
        removed = {disintegrated}
        queue = [disintegrated]
        while queue:
            for supported in supporting[queue.pop()]:
                if not (supported_by[supported] - removed):
                    removed.add(supported)
                    if supported in supporting:
                        queue.append(supported)
        falling += len(removed) - 1
    return falling


def stack_bricks(filename: str) -> tuple[int, dict[int, set[int]], dict[int, set[int]]]:
    with open(filename) as file:
        pieces = []
        for line in file:
            first, second = line.rstrip().split("~")
            x1, y1, z1 = map(int, first.split(","))
            x2, y2, z2 = map(int, second.split(","))
            pieces.append((z1, z2 - z1, x1, x2 - x1, y1, y2 - y1))
    filled = {}
    supported_by = defaultdict(set)
    supporting = defaultdict(set)
    for p, (z1, dz, x1, dx, y1, dy) in enumerate(sorted(pieces)):
        sx, sy, sz = (1 if d else 0 for d in (dx, dy, dz))
        drop = z1 - 1
        blocks = []
        for i in range(max(dx, dy, dz) + 1):
            xy, z = (x1 + i * sx, y1 + i * sy), z1 + i * sz
            blocks.append((xy, z))
            if xy in filled:
                new_drop = z - filled[xy][0] - 1
                if new_drop < drop:
                    drop = new_drop
        for xy, z in blocks:
            if xy in filled:
                sz, sp = filled[xy]
                if sz == z - drop - 1 and sp != p:
                    supported_by[p].add(sp)
                    supporting[sp].add(p)
            filled[xy] = (z - drop, p)
    return len(pieces), supported_by, supporting
