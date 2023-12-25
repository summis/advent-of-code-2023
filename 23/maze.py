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


from collections import defaultdict


def create_condensed_graph(input_file):
    vertices = {complex(i, j): x for j, row in enumerate(open(input_file).read().splitlines()) for i, x in enumerate(row) if x != "#"}
    edges = {}

    
    list_of_vertices = list(vertices.keys())
    for i, v1 in enumerate(list_of_vertices):
        for v2 in list_of_vertices[i+1:]:
            if abs(v1 - v2) == 1:
                edges[(v1, v2)] = 1

    # Condense
    reference_counts = {z: 0 for z in vertices}
    for x, y in edges:
        reference_counts[x] += 1
        reference_counts[y] += 1

    for z in vertices:
        if reference_counts[z] == 2:
            [e1, e2] = [e for e in edges if z in e]
            e3 = tuple(x for x in (*e1,*e2) if x != z)
            edges[e3] = edges[e2] + edges[e1]

            del edges[e1], edges[e2]

    expanded = defaultdict(lambda: {})
    for (z1, z2), d in edges.items():
        expanded[z1][z2] = d
        expanded[z2][z1] = d

    return dict(expanded)


def search(start, end, graph):
    paths = [(0, [start])]

    while paths:
        step_count, path = paths.pop(-1)

        for dest, distance in graph[path[-1]].items():
            if dest in path:
                continue

            new = path + [dest]
            if dest == end:
                yield step_count + distance
            else:
                paths.append((step_count + distance, new))
            

def test_part_1():
    best = max(walk(input_file="toy", start=complex(1, 0), end=complex(21, 22)), key=len)
    assert len(best) - 1 == 94


def part1():
    best = max(walk(input_file="real", start=complex(1, 0), end=complex(139, 140)), key=len)
    return len(best) - 1


def test_part_2():
    graph = create_condensed_graph(input_file="toy")
    assert max(search(start=complex(1, 0), end=complex(21, 22), graph=graph)) == 154


# Runtime ~ 1min
def part2():
    graph = create_condensed_graph(input_file="real")
    return max(search(start=complex(1, 0), end=complex(139, 140), graph=graph))


test_part_1()
test_part_2()


print(part1(), part2())