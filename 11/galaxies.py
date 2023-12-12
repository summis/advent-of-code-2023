import numpy as np
from itertools import combinations


with open("input") as f:
    data = f.read().splitlines()


def expand_vertically(data):
    expanded = []
    for row in data:
        if all(x == "." for x in row):
            expanded.append(row)
        expanded.append(row)
    return expanded


def transpose(data):
    return ["".join(a) for a in zip(*data)]


expanded_data = transpose(expand_vertically(transpose(expand_vertically(data))))


def distance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])


def part1():
    A = np.array([[x for x in y] for y in expanded_data])
    [y], [x] = zip(np.where(A == "#"))
    coordinates = zip(y, x)
    pairs = combinations(coordinates, 2)

    print(sum(map(lambda x: distance(x[0], x[1]), pairs)))


def get_empty_rows(data):
    return [i for i, row in enumerate(data) if all(x == "." for x in row)]


empty_rows = get_empty_rows(data)
empty_columns = get_empty_rows(transpose(data))


def part2():
    coordinates = []
    for j, row in enumerate(data):
        for i, character in enumerate(row):
            if character == "#":
                y = j
                x = i
                for limit in empty_rows:
                    if j > limit:
                        y += 999999
                for limit in empty_columns:
                    if i > limit:
                        x += 999999
                coordinates.append((y, x))

    print(sum(map(lambda x: distance(x[0], x[1]), combinations(coordinates, 2))))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
        