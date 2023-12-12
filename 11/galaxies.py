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


def main():
    part1()


if __name__ == "__main__":
    main()
        
