

def calc_distance(t, x):
    return x * t - x * x

def part1():
    with open("input") as f:
        data = f.read().splitlines()

    times = map(int, data[0].split(":")[1].strip().split())
    distances = list(map(int, data[1].split(":")[1].strip().split()))

    total_product = 1

    for i, time in enumerate(times):
        d = distances[i]
        total_product *= len([x for x in range(time) if calc_distance(time, x) > d])

    print(total_product)


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()