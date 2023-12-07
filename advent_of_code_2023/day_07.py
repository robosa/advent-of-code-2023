from collections import Counter

CARDS_EASY = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
CARDS_HARD = {"A": 14, "K": 13, "Q": 12, "J": 0, "T": 10}


def run(filename: str, hard: bool) -> int:
    hands = []
    cards = CARDS_HARD if hard else CARDS_EASY
    with open(filename, "r") as file:
        for line in file:
            hand, bid = line.split()
            hand = [cards[c] if c in cards else int(c) for c in hand]
            hands.append(((get_rank(hand), *hand), int(bid)))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(sorted(hands)))


def get_rank(hand: list[int]) -> int:
    counts = Counter(hand)
    match len(counts.keys()), max(counts.values()), counts[0]:
        case (5, _, 0):
            return 0
        case (4, _, 0) | (5, _, _):
            return 1
        case (3, 2, 0):
            return 2
        case (3, _, 0) | (4, _, _):
            return 3
        case (2, 3, 0) | (3, 2, 1):
            return 4
        case (2, _, 0) | (3, _, _):
            return 5
        case _:
            return 6
