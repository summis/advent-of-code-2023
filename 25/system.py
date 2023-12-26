import math


def read_data(filename):
    G = {}
    for key, connections in (x.split(":") for x in open(filename).read().splitlines()):
        for connection in connections.split():
            if key in G:
                G[key][connection] = 1
            else:
                G[key] = {connection: 1}
            
            if connection in G:
                G[connection][key] = 1
            else:
                G[connection] = {key: 1}

    V = set(G.keys())

    return V, G

# Problem is minimum cut finding problem.
# Solved with Stoer-Wagner algorithm https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm


import itertools

from heapq import heappush, heappop

# V = Set of vertices
# G = Graph giving connections
def minimum_cut_phase(V, G):

    # Heap queue with possibility to update task priority
    # https://docs.python.org/3/library/heapq.html
    pq = []                         # list of entries arranged in a heap
    entry_finder = {}               # mapping of tasks to entries
    REMOVED = '<removed-task>'      # placeholder for a removed task
    counter = itertools.count()     # unique sequence count

    def add_task(task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in entry_finder:
            remove_task(task)
        count = next(counter)
        entry = [priority, count, task]
        entry_finder[task] = entry
        heappush(pq, entry)

    def remove_task(task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task():
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while pq:
            priority, count, task = heappop(pq)
            if task is not REMOVED:
                del entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    # Stoer-Wagner starts
    v = list(V)[0]
    A = [v]

    for k in G[v]:
        add_task(k, priority=-sum(vv for kk, vv in G[k].items() if kk in A))

    while len(A) != len(V):
        # Find the most tightly connected vertex
        x = pop_task()
        cut_value = sum(vv for kk, vv in G[x].items() if kk in A)

        A.append(x)

        for k in G[x]:
            if k not in A:
                add_task(k, priority=-sum(vv for kk, vv in G[k].items() if kk in A))
        

    last = A[-1]
    before_last = A[-2]
    # Store names to new name
    new_node = before_last + "+" + last

    # Update vertices 
    V.add(new_node)
    V.remove(last)
    V.remove(before_last)

    # Update graph
    # Create new node and delete old nodes
    G[new_node] = {
        k: v for k, v in G[last].items() if k != before_last
    }
    for k, v in G[before_last].items():
        if k == last:
            continue

        if k in G[new_node]:
            G[new_node][k] += v 
        else:
            G[new_node][k] = v

    del G[last]
    del G[before_last]


    # For all vertices to which `last` and `before_last` are connected, update reference and weight
    for k, v in G[new_node].items():
        if last in G[k]: del G[k][last]
        if before_last in G[k]: del G[k][before_last]
        G[k][new_node] = v

    return last, cut_value


def minimum_cut(V, G):
    best_cut = (None, math.inf)


    iter = 0
    while len(V) > 1:
        print("Iteration", iter)
        new_cut = minimum_cut_phase(V, G)

        if new_cut[1] < best_cut[1]:
            best_cut = new_cut

        iter += 1

    return best_cut



def part1():
    V, G = read_data("real")
    n = len(V)
    joined, min_cut = minimum_cut(V, G)

    print(joined, min_cut)
    assert min_cut == 3
    k = len(joined.split("+"))
    return (n-k) * k


print(part1())