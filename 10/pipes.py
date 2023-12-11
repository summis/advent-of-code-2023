import numpy as np
import enum
import sys
from itertools import product

sys.setrecursionlimit(15000)

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
    path = [(y, x)]

    while True:
        dy, dx = delta[to]
        y += dy
        x += dx
        path.append((y, x))

        c = A[y, x]

        if c == "S":
            break

        to = next_direction[to][c]

    return path 


def part1():
    # By visual inspection, "J" is the only fitting start character
    path = follow_path((start_y, start_x), "J", Directions.NORTH)
    print( (len(path) - 2) // 2 + 1  )


def sum_points(x, y):
    return (x[0] + y[0], x[1] + y[1])


def flood_and_fill(point, candidates):
    ret = set([point])
    
    def inner(point):
        for direction in Directions:
            new_point = sum_points(point, delta[direction])
            if new_point in candidates:
                candidates.remove(new_point)
                ret.add(new_point)
                inner(new_point)

    inner(point)
    return ret


def part2():
    y_len, x_len = A.shape
    points = set(product(range(y_len), range(x_len)))
    loop = follow_path((start_y, start_x), "J", Directions.NORTH)
    
    candidates = points - set(loop)

    regions = []
    while len(candidates):
        point = candidates.pop()
        new_set = flood_and_fill(point, candidates)
        regions.append(new_set)

    points_inside = 0
    for region in regions:
        y, x = region.pop()
        left_and_in_loop = [(y, i) for i in range(x) if (y, i) in loop]

        up_count = 0
        prev_char = None
        for point in left_and_in_loop:
            if A[point] == "|":
                up_count += 1

            if A[point] in "L":
                prev_char = "L"
            
            if A[point] == "F":
                prev_char = "F"

            if A[point] in "7":
                if prev_char == "L":
                    up_count += 1
                    prev_char = None
                if prev_char == "F":
                    up_count += 2
                    prev_char = None

            if A[point] in "J":
                if prev_char == "L":
                    up_count += 2
                    prev_char = None
                if prev_char == "F":
                    up_count += 1
                    prev_char = None

        if up_count % 2 == 1:
            points_inside += len(region) + 1

    print(points_inside)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()