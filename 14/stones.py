with open("input") as f:
    data = f.read().splitlines()


def transpose(data):
    return ["".join(a) for a in zip(*data)]


def move(l):
    free_space_left_side = 0
    l = [*l]

    for i in range(len(l)):
        c = l[i]

        if c == ".":
            free_space_left_side += 1

        if c == "#":
            free_space_left_side = 0
        
        if c == "O":
            l[i] = l[i - free_space_left_side]
            l[i - free_space_left_side] = "O"
    
    return "".join(l)


assert move("...O") == "O..."
assert move(".#.O") == ".#O."
assert move("..OO") == "OO.."
assert move(".....O#O..O") == "O.....#OO.."


def count(l):
    total = 0

    for i, c in enumerate(l):
        if c == "O":
            total += len(l) - i
    
    return total


assert count("O...") == 4
assert count(".#O.") == 2
assert count("OO..") == 7
assert count("O.....#OO..") == 18


def part1():
    moved_data = [move(l) for l in transpose(data)]
    print(sum(count(x) for x in moved_data))


def rotate(data):
    return list(reversed(transpose(data)))


assert rotate(["abc", "def", "ghi"]) == ["cfi", "beh", "adg"]
assert rotate(rotate(rotate(rotate(["abc", "def", "ghi"])))) == ["abc", "def", "ghi"]
assert rotate(["cfi", "beh", "adg"]) == ["ihg", "fed", "cba"]


def run_cycle(data):
    # North 
    data = [move(l) for l in data]

    # West
    data = rotate(rotate(rotate(data)))
    data = [move(l) for l in data]

    # South
    data = rotate(rotate(rotate(data)))
    data = [move(l) for l in data]

    # East 
    data = rotate(rotate(rotate(data)))
    data = [move(l) for l in data]

    # Restore north orientation
    return rotate(rotate(rotate(data)))


def test_cycle():
    input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    grid = rotate(input.splitlines())

    grid = run_cycle(grid)
    assert "\n".join(rotate(rotate(rotate(grid)))) == """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

    grid = run_cycle(grid)
    assert "\n".join(rotate(rotate(rotate(grid)))) == """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""

    grid = run_cycle(grid)
    assert "\n".join(rotate(rotate(rotate(grid)))) == """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""


test_cycle()


def part2():
    grid = rotate(data) # North pointing left
    
    iterations = []
    grid = run_cycle(grid)
    iterations.append(grid)
    grid = run_cycle(grid)
    iterations.append(grid)

    tortoise = 0
    hare = 1

    while iterations[tortoise] != iterations[hare]:
        grid = run_cycle(grid)
        iterations.append(grid)
        grid = run_cycle(grid)
        iterations.append(grid)
        tortoise += 1
        hare += 2

    target = 1000000000
    period = hare - tortoise
    repeats = (target - (hare + 1)) % period 

    for _ in range(repeats):
        grid = run_cycle(grid)

    print(sum(count(x) for x in grid))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()