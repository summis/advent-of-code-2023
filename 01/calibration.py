# https://adventofcode.com/2023/day/1

import argparse

NUMBERS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4, 
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def reverse_string(string: str) -> str:
    return string[::-1]


REVERSED_NUMBERS = {
    reverse_string(key): val for key, val in NUMBERS.items()
}


def get_first_digit_in_lookup(input_string: str, number_lookup: "dict[str, int]") -> int:
    hits = {}

    for number in number_lookup:
        index = input_string.find(number)
        if index != -1:
            hits[number] = index

    return number_lookup[min(hits, key=hits.get)]


def get_first_digit(input_string: str) -> int:
    return get_first_digit_in_lookup(input_string, NUMBERS)


def get_second_digit(input_string: str) -> int:
    return get_first_digit_in_lookup(reverse_string(input_string), REVERSED_NUMBERS)


def calibrator_v2(input_string: str) -> int:
    first_digit = get_first_digit(input_string)
    second_digit = get_second_digit(input_string)
    return 10 * first_digit + second_digit


def calibrator(input_string: str) -> int:
    first_digit = next((char for char in input_string if char.isnumeric()), None)
    second_digit = next((char for char in reversed(input_string) if char.isnumeric()), None)
    return int(f"{first_digit}{second_digit}")


def main():
    parser = argparse.ArgumentParser(description='Calculate sum of first and last digits in each line of a file.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('--spelled-numbers', action='store_true', help='Consider also spelled number, eg. "one", "two"')

    args = parser.parse_args()

    total_sum = 0

    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                if args.spelled_numbers:
                    result = calibrator_v2(line)
                else:
                    result = calibrator(line)
                total_sum += result

    print(f"Total sum of first and last digits in the file: {total_sum}")

if __name__ == "__main__":
    main()