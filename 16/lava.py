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


def part1():
    visited_paths = set()
    visited_points = set()

    def walk(point, direction):
        if (point, direction) in visited_paths: return
        if not point_in_grid(point): return

        visited_paths.add((point, direction))
        visited_points.add(point)
        
        element = tiles[point]

        for new_direction in continuations[(element, direction)]:
            new_point = calculate_new_point(point, new_direction)
            walk(new_point, new_direction)
    
    walk((0, 0), "east")
    print(len(visited_points))


part1()

