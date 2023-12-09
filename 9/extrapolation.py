with open("input") as f:
    data = [list(map(int, x.split())) for x in f.read().splitlines()]


def diffs(l):
    return [x-y for x,y in zip(l[1:], l[:-1])]


def next_value(l):
    if all(x==0 for x in l): return 0
    return l[-1] + next_value(diffs(l))


def part1():
    print(sum(next_value(x) for x in data))
    

def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()