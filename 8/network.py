


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


def part2():
    pass


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()