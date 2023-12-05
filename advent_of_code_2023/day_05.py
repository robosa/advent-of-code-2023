Map = list[tuple[int, int, int]]
Ranges = list[tuple[int, int]]


def run(filename: str, hard: bool) -> int:
    seeds, maps = parse_input(filename)
    if not hard:
        return min(get_location(seed, maps) for seed in seeds)
    ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for map in maps:
        ranges = map_ranges(ranges, map)
    return min(ranges)[0]


def parse_input(filename: str) -> tuple[list[int], list[Map]]:
    with open(filename, "r") as file:
        seeds = [int(i) for i in file.readline().split(":")[1].split()]
        file.readline()
        file.readline()
        maps = []
        map = []
        for line in file:
            if line == "\n":
                file.readline()
                maps.append(sorted(map))
                map = []
            else:
                dest, source, n = (int(i) for i in line.split())
                map.append((source, source + n, dest - source))
        maps.append(sorted(map))
    return seeds, maps


def get_location(seed: int, maps: list[Map]) -> int:
    current = seed
    for map in maps:
        for source, end, offset in map:
            if current < end:
                if current >= source:
                    current += offset
                break
    return current


def map_ranges(ranges: Ranges, map: Map) -> Ranges:
    mapped_ranges = []
    for start, length in ranges:
        for source, end, offset in map:
            if start < source:
                overlap = min(length, source - start)
                mapped_ranges.append((start, overlap))
                length -= overlap
                if not length:
                    break
                start = source
            if start < end:
                overlap = min(length, end - start)
                mapped_ranges.append((start + offset, overlap))
                length -= overlap
                if not length:
                    break
                start = end
        if length:
            mapped_ranges.append((start, length))
    return mapped_ranges
