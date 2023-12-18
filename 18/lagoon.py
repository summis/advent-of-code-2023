import sys

sys.setrecursionlimit(150000)



with open("input") as f:
    data = f.read().splitlines()

directions = (1, -1, 1j, -1j)
lookup = {
    "L": -1,
    "U": 1j,
    "D": -1j,
    "R": 1
}

def parse_line(data):
    prev = complex(0, 0)
    result = set([prev])

    for [direction, _repeats, _] in (x.split() for x in data):
        for _ in range(int(_repeats)):
            new = prev + lookup[direction]
            result.add(new)
            prev = new
        
    return result


def flood_and_fill(start, candidates):
    ret = set()
    start_points = set([start])
        
    while len(start_points):
        point = start_points.pop()
        ret.add(point)
        for direction in directions:
            new = point + direction
            if new in candidates:
                candidates.remove(new)
                start_points.add(new)
        
    return ret


# 48653 is too high
# 48652 is correct, using set when parsing cycle helped :)
def part1():
    path = parse_line(data)

    j_min = int(min(z.imag for z in path))
    j_max = int(max(z.imag for z in path))
    i_min = int(min(z.real for z in path))
    i_max = int(max(z.real for z in path))

    # Add "frame" to connect all outside regions
    points = set(complex(i, j) for i in range(i_min -1, i_max + 2) for j in range(j_min -1, j_max + 2)) - set(path)

    # visualization = ""
    # for j in range(j_min-1, j_max + 2):
    #     for i in range(i_min-1, i_max + 2):
    #         if complex(i, j) in path:
    #             visualization += "#"
    #         else:
    #             visualization += "."
    #     visualization += "\n"
    # print(visualization)

    regions = []
    while len(points):
        point = points.pop()
        regions.append(flood_and_fill(point, points))
    
    # Insight from data: there are only two regions -> only one "inside" and one "outside"
    inner_region = [x for x in regions if complex(i_min-1, j_min -1) not in x][0]
    print(len(inner_region) + len(path))


part1()