from collections import defaultdict
import math

labels = "A K Q J T 9 8 7 6 5 4 3 2".split()
base_number = len(labels)
label_scores = {
    label: base_number - i for i, label in enumerate(labels)
}


def _get_hands():
    with open("input") as f:
        data = f.read().splitlines()

    hands = {}

    for row in data:
        [hand, bid] = row.split()
        hands[hand] = int(bid)

    return hands


def _score_hand(hand):
    counts = defaultdict(int)

    for card in hand:
        counts[card] += 1

    primary = sum(math.pow(10, x) for x in counts.values())
    secondary = tuple(label_scores[card] for card in hand)

    return (primary, secondary)


def part1():
    hands = _get_hands()
    ranked_hands = sorted(hands.keys(), key=_score_hand)

    total = 0
    rank = 1
    for hand in ranked_hands:
        total += hands[hand] * rank
        rank += 1

    print(total)


def part2():
    labels = "A K Q T 9 8 7 6 5 4 3 2 J".split()
    base_number = len(labels)
    label_scores = {
        label: base_number - i for i, label in enumerate(labels)
    }

    def _score_hand2(hand):
        counts = defaultdict(int)
        jokers = 0

        for card in hand:
            if card != "J":
                counts[card] += 1
            else:
                jokers += 1

        if counts:
            counts[max(counts.keys(), key=counts.get)] += jokers
        else:
            counts["J"] = 5

        primary = sum(math.pow(10, x) for x in counts.values())
        secondary = tuple(label_scores[card] for card in hand)

        return (primary, secondary)

    hands = _get_hands()
    ranked_hands = sorted(hands.keys(), key=_score_hand2)

    total = 0
    rank = 1
    for hand in ranked_hands:
        total += hands[hand] * rank
        rank += 1

    print(total)

def main():
    part1()
    part2()


if __name__ == "__main__":
    main()