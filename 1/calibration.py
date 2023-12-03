# https://adventofcode.com/2023/day/1

import argparse


def calibrator(input_string: str) -> int:
    first_digit = next((char for char in input_string if char.isnumeric()), None)
    second_digit = next((char for char in reversed(input_string) if char.isnumeric()), None)
    return int(f"{first_digit}{second_digit}")


def main():
    parser = argparse.ArgumentParser(description='Calculate sum of first and last digits in each line of a file.')
    parser.add_argument('input_file', help='Path to the input file')

    args = parser.parse_args()

    total_sum = 0

    with open(args.input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                result = calibrator(line)
                total_sum += result

    print(f"Total sum of first and last digits in the file: {total_sum}")

if __name__ == "__main__":
    main()