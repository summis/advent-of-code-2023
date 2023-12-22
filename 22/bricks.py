def parse_blocks():
    blocks = {}
    for id, row in enumerate(open("input").read().splitlines()):
        [start, end] = row.split("~")

        [xs, ys, zs] = list(map(int, start.split(",")))
        [xe, ye, ze] = list(map(int, end.split(",")))

        blocks[id] = ((xs, ys, zs), (xe, ye, ze))

    return blocks


# The lower the z-coordinate, the sooner it hits the ground
def sorted_block_ids(blocks):
    return sorted(blocks.keys(), key=lambda x: blocks[x][0][2])


def parse_graph(block_ids, blocks):
    layout = {}
    graph = {"ground": {"supports": set(), "supported_by": set()}}

    for id in block_ids:
        ((xs, ys, zs), (xe, ye, ze)) = blocks[id]

        # Figure out where x and y overlap with layout
        projection_on_ground = [
            (x, y) for x in range(xs, xe + 1) for y in range(ys, ye + 1)
        ]
        exising_points_on_projection = [
            point for point in layout if (point[0], point[1]) in projection_on_ground
        ]

        # No block below, ground supports
        if not exising_points_on_projection:
            zs_new = 1
            ze_new = ze - zs + 1

            for z in range(zs_new, ze_new + 1):
                for x, y in projection_on_ground:
                    layout[(x, y, z)] = id

            graph["ground"]["supports"].add(id)
            graph[id] = {"supports": set(), "supported_by": set([id])}
        else:
            ground_level = max(z for _, _, z in exising_points_on_projection)
            supporting_blocks = set(
                layout[point]
                for point in exising_points_on_projection
                if point[2] == ground_level
            )

            for block in supporting_blocks:
                graph[block]["supports"].add(id)

            graph[id] = {"supports": set(), "supported_by": supporting_blocks}

            zs_new = ground_level + 1
            ze_new = ze - zs + zs_new

            for z in range(zs_new, ze_new + 1):
                for x, y in projection_on_ground:
                    layout[(x, y, z)] = id

    return graph


def part1():
    blocks = parse_blocks()
    block_ids = sorted_block_ids(blocks)
    graph = parse_graph(block_ids, blocks)

    return sum(
        len(x["supports"]) == 0
        or all(len(graph[id]["supported_by"]) > 1 for id in x["supports"])
        for x in graph.values()
    )


def count_cascade(graph, id):
    would_fall = set([id])
    candidates = graph[id]["supports"].copy()

    while candidates:
        candidate = candidates.pop()
        
        if graph[candidate]["supported_by"].issubset(would_fall):
            would_fall.add(candidate)
            candidates = candidates.union(graph[candidate]["supports"])

    return len(would_fall) - 1 # Exclude the first removed brick


def part2():
    blocks = parse_blocks()
    block_ids = sorted_block_ids(blocks)
    graph = parse_graph(block_ids, blocks)

    return sum(count_cascade(graph, id) for id in graph if id != "ground")


print(part1(), part2())
