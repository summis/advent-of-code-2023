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
import cmath

from queue import PriorityQueue

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class HeatLossPrioritizedState:
    heat: int
    state: Any=field(compare=False)


with open("/home/summis/advent-of-code-2023/17/input") as f:
    graph = {complex(i, j): int(weight) for j, row in enumerate(f.read().splitlines()) for i, weight in enumerate(row)}

directions = (1, -1, 1j, -1j)



def djikstra(graph, start, allowed_consecutive_steps):
    initial_state = (start, 0)

    heat_loss = {}  # Cost of getting to square when coming from certain direction
    todo = PriorityQueue()
    states = [(node, lenght * step) for node in graph for step in directions for lenght in allowed_consecutive_steps] + [initial_state]

    for _state in states:
        heat_loss[_state] = 0 if _state == initial_state else math.inf
        todo.put(HeatLossPrioritizedState(heat_loss[_state], _state))

    previous = {}  # Stores solution

    while not todo.empty():
        min_cost_state = todo.get().state
        node, route = min_cost_state

        for (step, repeats) in ((direction , length) for length in allowed_consecutive_steps for direction in directions):
            if route and cmath.phase(-route) == cmath.phase(step): continue

            neighbor = node + repeats * step

            if neighbor not in graph: continue

            if cmath.phase(route) == cmath.phase(step):
                route_to_neighbor = route + repeats * step 
            else:
                route_to_neighbor = repeats * step 

            if abs(route_to_neighbor) > allowed_consecutive_steps[-1]: continue

            loss = heat_loss[min_cost_state] + sum(graph[node + i * step] for i in range(1, repeats+1))
            neighbor_state = (neighbor, route_to_neighbor)

            if loss < heat_loss[neighbor_state]:
                heat_loss[neighbor_state] = loss
                previous[neighbor_state] = min_cost_state
                todo.put(HeatLossPrioritizedState(loss, neighbor_state))

    return previous, heat_loss


def part1():
    start = complex(0, 0)
    end = complex(140, 140)
    allowed_consecutive_tiles = (1, 2, 3)
    paths, losses = djikstra(graph, start, allowed_consecutive_tiles)

    ends = [(_end, d) for (_end, d) in paths if _end == end]

    heat_losses = [losses[x] for x in ends]
    best_path = min(range(len(heat_losses)), key=heat_losses.__getitem__)

    parsed_path = []
    for x in ends:
        full_path = []
        while x in paths:
            s, _ = x
            full_path = [s] + full_path
            x = paths[x]
        parsed_path.append(full_path)

    visualization = ""
    for j in range(int(end.imag)+1):
        for i in range(int(end.real)+1):
            if complex(i, j) in parsed_path[best_path]:
                visualization += "#"
            else:
                visualization += "."
        visualization += "\n"

    print(heat_losses[best_path])
    print(visualization)



# same as part 1 but neighbors are 4 - 10 steps away
def part2():
    start = complex(0, 0)
    end = complex(140, 140)
    allowed_consecutive_tiles = (4, 5, 6, 7, 8, 9, 10)
    paths, losses = djikstra(graph, start, allowed_consecutive_tiles)

    ends = [(_end, d) for (_end, d) in paths if _end == end]

    heat_losses = [losses[x] for x in ends]

    print(heat_losses)
    best_path = min(range(len(heat_losses)), key=heat_losses.__getitem__)

    parsed_path = []
    for x in ends:
        full_path = []
        while x in paths:
            s, _ = x
            full_path = [s] + full_path
            x = paths[x]
        parsed_path.append(full_path)

    visualization = ""
    for j in range(int(end.imag)+1):
        for i in range(int(end.real)+1):
            if complex(i, j) in parsed_path[best_path]:
                visualization += "#"
            else:
                visualization += "."
        visualization += "\n"

    print(heat_losses[best_path])
    print(visualization)


part1()
part2()
