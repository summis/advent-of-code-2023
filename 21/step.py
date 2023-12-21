import numpy as np


graph = {complex(i, j): c for j, row in enumerate(open("input").read().splitlines()) for i, c in enumerate(row)}
directions = (1, -1, 1j, -1j)
starts = [x for x in graph if graph[x] == "S"]


def propagate(starts, n):
    starts = set(starts)
    ends_up = set()

    for _ in range(n):
        while starts:
            s = starts.pop()
            for d in directions:
                if graph[s+d] != "#":
                    ends_up.add(s+d)

        starts = ends_up
        ends_up = set()
    
    return starts


def part1():
    return len(propagate(starts, 64))


print(part1())