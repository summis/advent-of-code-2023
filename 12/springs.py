from functools import lru_cache

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


@lru_cache
def count_valid_solutions(s, key, index):
    if s == "": return index == len(key)
    
    s1, s2 = s[0], s[1:]
    if s1 == ".": return count_valid_solutions(s2, key, index)

    if s1 == "#":
        if index == len(key): return 0

        n = key[index]
        s3, s4 = s[:n], s[n:]
        if (len(s3) == n and "." not in s3):
            if s4 == "" or s4[0] == ".": return count_valid_solutions(s4, key, index + 1)
            if s4[0] == "?": return count_valid_solutions("."+s4[1:], key, index + 1)
        return 0

    return count_valid_solutions("#"+s2, key, index) + count_valid_solutions("."+s2, key, index)


assert count_valid_solutions("#...##..#..", (1, 2, 1), 0) == 1
assert count_valid_solutions("??..##..#..", (1, 2, 1), 0) == 2
assert count_valid_solutions("??..##..?", (1, 2, 1), 0) == 2
assert count_valid_solutions("??..##..??", (1, 2, 1), 0) == 4
assert count_valid_solutions("??..##..???", (1, 2, 1), 0) == 6
assert count_valid_solutions("?????", (2,), 0) == 4
assert count_valid_solutions("", (2,), 0) == 0
assert count_valid_solutions("??", (2,), 0) == 1
assert count_valid_solutions("????", (1,), 0) == 4


def part2():
    solution_count = 0

    for i, row in enumerate(data):
        raw_string, raw_key = row.split()

        raw_string = "?".join(5 * [raw_string])
        raw_key = ",".join(5 * [raw_key])
        
        key = tuple(int(x) for x in raw_key.split(","))
        solution_count += count_valid_solutions(raw_string, key, 0)

        if i % 10 == 0:
            print(f"Iteration {i}, solution count {solution_count}")

    print(solution_count)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()