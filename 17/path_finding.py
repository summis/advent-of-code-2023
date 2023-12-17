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
from collections import defaultdict

with open("input") as f:
    graph = {complex(i, j): int(weight) for j, row in enumerate(f.read().splitlines()) for i, weight in enumerate(row)}


# TODO: constraint
def djikstra(graph, start, end):
    heat_loss = {z: math.inf for z in graph}
    heat_loss[start] = 0

    todo = set(graph.keys())
    while todo:
        closest = min(todo, key=heat_loss.get)
        if closest == end:
            return heat_loss[closest]
        
        todo.remove(closest)

        for neighbor in [closest + d for d in (1, -1, 1j, -1j) if closest+d in graph]:
            loss_via_path = heat_loss[closest] + graph[neighbor]
            if loss_via_path < heat_loss[neighbor]:
                heat_loss[neighbor] = loss_via_path
    
    return -1


def part1():
    # print(djikstra(graph, complex(0, 0j), complex(140, 140)))
    print(djikstra(graph, complex(0, 0j), complex(12, 12)))


part1()
