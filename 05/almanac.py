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


def apply_mapping(_range, mapping):
    start, end = _range
    dest, src, lenght = mapping
    
    s1 = max(start, min(src, end))
    s2 = min(end, max(src + lenght, start))
    
    return (start, s1), (s1, s2), (s2, end), (s1 + dest-src, s2 + dest-src)


def not_empty(_range):
    start, end = _range
    return start < end


def apply_map_to_range(ranges, map):
    input_ranges = ranges
    output_ranges = set()

    for mapping in map:
        inputs_for_next_round = set()
        for _range in input_ranges:
            i1, _, i2, o = apply_mapping(_range, mapping)

            if not_empty(o):
                output_ranges.add(o)

            if not_empty(i1):
                inputs_for_next_round.add(i1)

            if not_empty(i2):
                inputs_for_next_round.add(i2)
        
        input_ranges = inputs_for_next_round

    
    return output_ranges.union(inputs_for_next_round)
            

def part2():
    with open("input") as f:
        data = f.read().split("\n\n")
        _ranges = [int(x) for x  in data[0].split(":")[1].strip().split()]

    starts = [x for i, x in enumerate(_ranges) if i % 2 == 0]
    lengths = [x for i, x in enumerate(_ranges) if i % 2 == 1]
    ranges = set(x for x in zip(starts, [x + y for x, y in zip(starts, lengths)]))
    maps = [parse_map(x) for x in data[1:]]

    print(min(x for x, _ in reduce(apply_map_to_range, maps, ranges)))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()