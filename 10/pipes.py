import numpy as np
import enum

with open("input") as f:
    data = [[x for x in y] for y in f.read().splitlines()]

A = np.array(data)
[start_y], [start_x] = np.where(A == "S")


class Directions(enum.Enum):
    NORTH = enum.auto()
    EAST = enum.auto()
    SOUTH = enum.auto()
    WEST = enum.auto()


next_direction = {
    Directions.SOUTH: {
        "|": Directions.SOUTH,
        "L": Directions.EAST,
        "J": Directions.WEST,
    },
    Directions.NORTH: {
        "|": Directions.NORTH,
        "7": Directions.WEST,
        "F": Directions.EAST
    },
    Directions.WEST: {
        "-": Directions.WEST,
        "L": Directions.NORTH,
        "F": Directions.SOUTH
    },
    Directions.EAST: {
        "-": Directions.EAST,
        "J": Directions.NORTH,
        "7": Directions.SOUTH,
    }
}

delta = {
    Directions.NORTH: (-1, 0),
    Directions.SOUTH: (1, 0),
    Directions.WEST: (0, -1),
    Directions.EAST: (0, 1)
}


def follow_path(start, start_character, to_direction):
    c = start_character
    to = to_direction
    y, x = start
    path = start_character

    while True:
        dy, dx = delta[to]
        y += dy
        x += dx

        c = A[y, x]
        path += c

        if c == "S":
            break

        to = next_direction[to][c]

    return path 


def part1():
    # By visual inspection, "J" is the only fitting start character
    path = follow_path((start_y, start_x), "J", Directions.NORTH)
    print( (len(path) - 2) // 2 + 1  )


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()