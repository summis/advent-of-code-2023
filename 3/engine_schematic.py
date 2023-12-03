# https://adventofcode.com/2023/day/3

import argparse

from io import TextIOWrapper

from typing import List, TypedDict, Set

from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])

Matrix = TextIOWrapper

class Number(TypedDict):
    value: int
    location: List[Point] 


def parse_special_character_locations(matrix: Matrix) -> Set[Point]:
    points = set()
    
    for j, row in enumerate(matrix):
        for i, char in enumerate(row):
            if char != "." and not char.isnumeric() and char != "\n":
                points.add(Point(i, j))

    return points


def calculate_neighborhood(location: List[Point]) -> Set[Point]:
    neighbors = set()

    for point in location:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                neighbor_x = point.x + i
                neighbor_y = point.y + j
                if neighbor_x >= 0 and neighbor_y >= 0:
                    neighbors.add(Point(neighbor_x, neighbor_y))
    
    return neighbors


def parse_numbers(matrix: Matrix) -> List[Number]:
    numbers = []

    for j, row in enumerate(matrix):
        current_location = None
        current_value = None
        for i, char in enumerate(row):
            if char.isnumeric():
                if current_location is None:
                    current_location = [Point(i, j)]
                    current_value = char
                else:
                    current_location.append(Point(i, j))
                    current_value += char
            else:
                if current_location is not None:
                    numbers.append(Number(value=int(current_value), location=current_location))
                    current_location = None
                    current_value = None

    return numbers


    


def main():
    parser = argparse.ArgumentParser(description="Return sum numbers adjanced to characters")
    parser.add_argument('input_file', help='Path to the input file')

    args = parser.parse_args()

    numbers = set()
    with open(args.input_file, 'r') as input_matrix:
        numbers = parse_numbers(input_matrix)

    special_chars = set()
    with open(args.input_file, 'r') as input_matrix:
        special_chars = parse_special_character_locations(input_matrix)

    total_sum = 0

    for number in numbers:
        if len(calculate_neighborhood(number["location"]).intersection(special_chars)) > 0:
            total_sum += number["value"]

    print(total_sum)
        


if __name__ == "__main__":
    main()