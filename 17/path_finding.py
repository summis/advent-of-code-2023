# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
#  1  function Dijkstra(Graph, source):
#  2      
#  3      for each vertex v in Graph.Vertices:
#  4          dist[v] ← INFINITY
#  5          prev[v] ← UNDEFINED
#  6          add v to Q
#  7      dist[source] ← 0
#  8      
#  9      while Q is not empty:
# 10          u ← vertex in Q with min dist[u]
# 11          remove u from Q
# 12          
# 13          for each neighbor v of u still in Q:
# 14              alt ← dist[u] + Graph.Edges(u, v)
# 15              if alt < dist[v]:
# 16                  dist[v] ← alt
# 17                  prev[v] ← u
# 18
# 19      return dist[], prev[]

import math

with open("/home/summis/advent-of-code-2023/17/input") as f:
    graph = {complex(i, j): int(weight) for j, row in enumerate(f.read().splitlines()) for i, weight in enumerate(row)}

directions = (1, -1, 1j, -1j)

import cmath

def djikstra(graph, start):
    previous = {}
    todo = set(
        (z, i*d) for z in graph.keys() for d in directions for i in (1, 2, 3) if z - i*d in graph
    ).union(((start, 0),))
    heat_loss = {z: math.inf for z in todo}
    heat_loss[(start, 0)] = 0

    while todo:
        closest = min(todo, key=heat_loss.get)
        z, f = closest
        todo.remove(closest)

        for d in directions:
            # Going back is not allowed
            if f and cmath.phase(-f) == cmath.phase(d): continue

            neighbor = z + d
            new_f = f + d if cmath.phase(f) == cmath.phase(d) else d

            # Out of bounds
            if neighbor not in graph: continue

            # Going too far
            if abs(new_f) > 3: continue

            loss_via_path = heat_loss[closest] + graph[neighbor]
            if loss_via_path < heat_loss[(neighbor, new_f)]:
                heat_loss[(neighbor, new_f)] = loss_via_path
                previous[(neighbor, new_f)] = closest

    return previous


def part1():
    # print(djikstra(graph, complex(0, 0j), complex(140, 140)))
    start = complex(0, 0)
    # end = complex(4, 3)
    end = complex(140, 140)
    end = complex(12, 12)
    path = djikstra(graph, start)

    ends = [(_end, d) for (_end, d) in path if _end == end]

    all_results = []
    for x in ends:
        full_path = []
        while x in path:
            s, _ = x
            full_path = [s] + full_path
            x = path[x]
        all_results.append(full_path)

    print(min(sum(graph[point] for point in l) for l in all_results))


    ret = ""
    for j in range(int(end.imag)+1):
        for i in range(int(end.real)+1):
            if complex(i, j) in all_results[2]:
                ret += "#"
            else:
                ret += "."
        ret += "\n"

    print(ret)


part1()
