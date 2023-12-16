import numpy as np
import sys
from collections import defaultdict

sys.setrecursionlimit(15000)


with open("input") as f:
    data = [[x for x in y] for y in f.read().splitlines()]

tiles = np.array(data)
Y_MAX, X_MAX = tiles.shape


def point_in_grid(point):
    y, x = point
    return 0 <= y < Y_MAX and 0 <= x < X_MAX


continuations = defaultdict(lambda x: [])
continuations.update({
    # "-"
    ("-", "south"): ["west", "east"],
    ("-", "north"): ["west", "east"],
    ("-", "east"): ["east"],
    ("-", "west"): ["west"],

    # "|"
    ("|", "south"): ["south"],
    ("|", "north"): ["north"],
    ("|", "east"): ["south", "north"],
    ("|", "west"): ["south", "north"],

    # "/"
    ("/", "south"): ["west"],
    ("/", "north"): ["east"],
    ("/", "east"): ["north"],
    ("/", "west"): ["south"],

    # "\\"
    ('\\', "south"): ["east"],
    ("\\", "north"): ["west"],
    ("\\", "east"): ["south"],
    ("\\", "west"): ["north"],
})
continuations.update({(".", x): [x] for x in ("north", "east", "south", "west")})


def calculate_new_point(point, direction):
    y, x = point
    if direction == "north": return (y - 1, x)
    if direction == "south": return (y + 1, x)
    if direction == "east": return (y, x + 1)
    if direction == "west": return (y, x - 1)

    print(direction)
    raise Exception("Invalid direction")


def energize(initial_point, initial_direction):
    visited_paths = set()
    visited_points = set()

    def walk(point, direction):
        if (point, direction) in visited_paths: return
        if not point_in_grid(point): return

        visited_paths.add((point, direction))
        visited_points.add(point)
        
        for new_direction in continuations[(tiles[point], direction)]:
            walk(calculate_new_point(point, new_direction), new_direction)
    
    walk(initial_point, initial_direction)
    return len(visited_points)


def part1():
    print(energize((0,0), "east"))


def part2():
    start_configurations = (
        [((y, 0), "east") for y in range(Y_MAX)]
        + [((y, X_MAX -1), "west") for y in range(Y_MAX)]
        + [((0, x), "south") for x in range(X_MAX)]
        + [((Y_MAX - 1, x), "north") for x in range(X_MAX)]
    )
    print(max(energize(point, direction) for point, direction in start_configurations))


part1()
part2()
