# https://adventofcode.com/2023/day/2

import argparse
from typing import List, TypedDict


class Round(TypedDict):
    red: int
    green: int
    blue: int

class Game(TypedDict):
    id: int
    rounds: List[Round]


def parse_game(game_string: str) -> Game:
    id_and_rounds = game_string.split(":")
    id = id_and_rounds[0][5:]
    _rounds = id_and_rounds[1].split(";")

    rounds = []

    for round in _rounds:
        results = Round(red=0, green=0, blue=0)

        colors = round.split(",")

        for _color in colors:
            count_and_color = _color.strip().split(" ")
            count = int(count_and_color[0])
            color = count_and_color[1]

            results[color] = count

        rounds.append(results)

    return Game(
        id=id,
        rounds=rounds
    )

        
def is_round_possible(round: Round) -> bool:
    return round["red"] <= 12 and round["green"] <=13 and round["blue"] <= 14


def is_game_possible(game: Game) -> bool:
    return all(is_round_possible(round) for round in game["rounds"])


class Bag(TypedDict):
    red: int
    green: int
    blue: int


def get_minimal_bag_enabling_game(game: Game) -> Bag:
    enabling_bag = Bag(red=0, green=0, blue=0)

    for round in game["rounds"]:
        for color in ["red", "green", "blue"]: 
            enabling_bag[color] = max(enabling_bag[color], round[color])

    return enabling_bag


def calculate_power_of_set(bag: Bag) -> int:
    return bag["blue"] * bag["green"] * bag["red"]


def main():
    parser = argparse.ArgumentParser(description="Return sum of ids of games that are possible.")
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('--count-powers', action='store_true', help='Calculates powers of bags')
    
    args = parser.parse_args()

    total_sum = 0
    
    with open(args.input_file, 'r') as file:
        for line in file:
            game = parse_game(line)
            if args.count_powers: 
                total_sum += calculate_power_of_set(get_minimal_bag_enabling_game(game))
            else:
                if is_game_possible(game):
                    total_sum += int(game["id"])

    print(total_sum)

if __name__ == "__main__":
    main()