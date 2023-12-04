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


def main():
    part1()


if __name__ == "__main__":
    main()