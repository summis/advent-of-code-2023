with open("input") as f:
    data = f.read().split("\n\n")


def find_horizontal_reflection_line(l):
    for i in range(1, len(l)):
        if is_reflection_index(l, i):
            return i
        
    return None


def transpose(data):
    return ["".join(a) for a in zip(*data)]


def is_reflection_index(l, n):
    assert 0 < n < len(l)
    return all(x == y for x, y in zip(reversed(l[:n]), l[n:]))


def part1():
    horizontal_total = 0
    vertical_total = 0

    for x in data:
        x =  x.splitlines()

        h = find_horizontal_reflection_line(x)
        if h:
            horizontal_total += h

        v = find_horizontal_reflection_line(transpose(x))
        if v:
            vertical_total += v

    print(100*horizontal_total + vertical_total)


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()