directions = (1, -1, 1j, -1j)


def get_graph(input_type):
    return {complex(i, j): c for j, row in enumerate(open(input_type).read().splitlines()) for i, c in enumerate(row) if c != "#"}


def propagate(graph, start, n):
    starts = set([start])
    ends_up = set()

    for _ in range(n):
        while starts:
            s = starts.pop()
            for d in directions:
                if s+d in graph:
                    ends_up.add(s+d)

        starts = ends_up
        ends_up = set()
    
    return starts


def test_part_1():
    graph = get_graph("toy")
    start = [x for x in graph if graph[x] == "S"][0]
    assert len(propagate(graph, start, 6)) == 16


def part1():
    graph = get_graph("real")
    start = [x for x in graph if graph[x] == "S"][0]
    return len(propagate(graph, start, 64))


import math


def bellman_ford(graph, start):
    distances = {z: math.inf for z in graph}
    distances[start] = 0

    # Enough many times
    for _ in range(400):
        for z in graph:
            if z == start:
                continue

            neighbors = [z + d for d in directions if z + d in graph]

            if neighbors:
                distances[z] = min(distances[n] for n in neighbors) + 1
        
    return distances



def neighbor_types(distances):
    types = {}
    for z in distances:
        neighbors = [z + d for d in directions if (z + d) in distances]

        if all(distances[x] % 2 == 0 for x in neighbors):
            types[z] = "Even"
        elif all(distances[x]  % 2 == 1 for x in neighbors):
            types[z] = "Odd"
        elif distances[z] == math.inf:
            types[z] = "Lonely"
        else:
            print(z, neighbors)
            types[z] = "Mixed"

    return types


# Shameless copy from https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
def part2():
    graph = get_graph("real")
    start = [x for x in graph if graph[x] == "S"][0]

    distances = bellman_ford(graph, start)
    reachable = {z for z,d in distances.items() if d != math.inf}

    even_full = {z for z in reachable if distances[z] % 2 == 0}
    even_corners = {z for z in even_full if distances[z] > 65}

    odd_full = {z for z in reachable if distances[z] % 2 == 1}
    odd_corners = {z for z in odd_full if distances[z] > 65}

    steps = 26501365
    N = 202300
    square_lenght = 131
    initial_steps = 65

    assert steps == N * square_lenght + initial_steps

    return (N + 1) * (N + 1) * len(odd_full) + N * N * len(even_full) - (N + 1) * len(odd_corners) + N * len(even_corners)


test_part_1()

print(part1(), part2())