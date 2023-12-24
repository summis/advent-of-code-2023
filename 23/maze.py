def walk(input_file, start, end, are_slopes_passable=False):
    maze = {complex(i, j): x for j, row in enumerate(open(input_file).read().splitlines()) for i, x in enumerate(row)}
    paths = [([start], 1j)]

    while paths:
        path, dir = paths.pop(0)

        for d in [1j * dir, dir, -1j * dir]:
            new_point = path[-1] + d

            # Prune not allowed and nonexistent paths
            if new_point not in maze:
                continue

            if maze[new_point] == "#":
                continue

            if not are_slopes_passable:
                if maze[new_point] == "^" and d == 1j: # A bit brain twister, up/down reversed when looking at input
                    continue

                if maze[new_point] == "v" and d == -1j:
                    continue

                if maze[new_point] == "<" and d == 1:
                    continue
                
                if maze[new_point] == ">" and d == -1:
                    continue

            # Can not cross path
            if new_point in path:
                continue

            new_path = path + [new_point]

            if new_point == end:
                yield new_path
            else:
                paths.append((new_path, d))


def test_part_1():
    best = max(walk(input_file="toy", start=complex(1, 0), end=complex(21, 22)), key=len)
    assert len(best) - 1 == 94


def part1():
    best = max(walk(input_file="real", start=complex(1, 0), end=complex(139, 140)), key=len)
    return len(best) - 1


# def test_part_2():
#     m, p = walk(input_file="toy", start=complex(1, 0), end=complex(21, 22), are_slopes_passable=True)
#     best = max(p, key=len)
#     assert len(best) - 1 == 154


# def part2():
#     m, p = walk(input_file="real", start=complex(1, 0), end=complex(139, 140), are_slopes_passable=True)
#     best = max(p, key=len)
#     return len(best) - 1


test_part_1()
# test_part_2()

print(part1())