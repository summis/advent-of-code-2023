with open("input") as f:
    data = f.read().splitlines()


def is_valid(s, key):
    return [len(x) for x in s.split(".") if x] == key


assert is_valid("#...##...", [1,2])
assert is_valid("#...##...###.#", [1,2,3,1])
assert not is_valid("#...##...", [1,3])


def _create_substrings(s):
    if s == "":
        return [""]
    elif s[0] == "?":
        return ["." + x for x in _create_substrings(s[1:])] +  ["#" + x for x in _create_substrings(s[1:])]
    else:
        return [s[0] + x for x in _create_substrings(s[1:])]


def part1():
    solution_count = 0

    for i, row in enumerate(data):
        raw_string, raw_key = row.split()
        candidates = _create_substrings(raw_string)
        key = [int(x) for x in raw_key.split(",")]
        solution_count += sum(is_valid(x, key) for x in candidates)

        if i % 10 == 0:
            print(f"Iteration {i}, solution count {solution_count}")

    print(solution_count)


def main():
    part1()
    # part2()


if __name__ == "__main__":
    main()