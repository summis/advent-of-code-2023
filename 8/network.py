import math
from functools import reduce


with open("input") as f:
    data = f.read().splitlines()

instructions = data[0]

network = {}
for connection in data[2:]:
    key, l, r = connection.replace("=", ",").replace("(", "").replace(")", "").replace(" ", "").split(",")
    network[key] = {
        "L": l,
        "R": r
    }


def part1():
    step_count = 0
    node = "AAA"

    while(node != "ZZZ"):
        node = network[node][instructions[step_count % len(instructions)]]
        step_count += 1

    print(step_count)


# https://stackoverflow.com/a/51716959
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def count_steps(start):
    step_count = 0
    while(start[-1] != "Z"):
        start = network[start][instructions[step_count % len(instructions)]]
        step_count += 1
    return step_count


def part2():
    nodes = [key for key in network if key[-1] == "A"]
    steps = [count_steps(node) for node in nodes]
    print(reduce(lcm, steps))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()