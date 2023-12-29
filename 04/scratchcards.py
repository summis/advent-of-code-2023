import math 


def part1():
    total = 0

    with open("input") as f:
        for line in f:
            [_id, numbers_string] = line.split(":")
            [ rewarded_numbers_string, card_numbers_string ] = numbers_string.split("|")

            rewarded_numbers = set(rewarded_numbers_string.split())
            card_numbers = set(card_numbers_string.split())
            hits = len(rewarded_numbers.intersection(card_numbers))

            if hits:
                total += math.pow(2, hits - 1)

    print(int(total))


def score(card: str) -> int:
    [_id, numbers_string] = card.split(":")
    [ rewarded_numbers_string, card_numbers_string ] = numbers_string.split("|")

    rewarded_numbers = set(rewarded_numbers_string.split())
    card_numbers = set(card_numbers_string.split())
    return len(rewarded_numbers.intersection(card_numbers))


def part2():
    cards = []
    with open("input") as f:
        cards = f.read().splitlines()

    visited_count = [1] * len(cards)

    for card_index, card in enumerate(cards):
        matches = score(card)
        for i in range(1, matches + 1):
            visited_count[card_index + i] += visited_count[card_index]

    print(sum(visited_count))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()