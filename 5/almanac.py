from functools import reduce


def parse_map(map):
    ranges = [x.split() for x in map.split("\n")[1:]]
    ranges = [(int(x), int(y), int(z)) for [x, y, z] in ranges]
    return ranges


def apply_map(num, map):
    for (dest, src, lenght) in map:
        if src <= num <= src + lenght:
            return dest + num - src
    return num


def part1():
    with open("input") as f:
        data = f.read().split("\n\n")
        seeds = [int(x) for x  in data[0].split(":")[1].strip().split()]
        maps = [parse_map(x) for x in data[1:]]

    print(min([
        reduce(apply_map, maps, x) for x in seeds
    ]))


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()