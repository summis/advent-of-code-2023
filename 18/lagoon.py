
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
    result = [prev]

    for [direction, _repeats, _] in (x.split() for x in data):
        for _ in range(int(_repeats)):
            new = prev + lookup[direction]
            result.append(new)
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
    print(len(inner_region) + len(set(path)))



def parse_line_2(data):
    prev = complex(0, 0)
    result = [prev]

    for [_, _, color] in (x.split() for x in data):
        hexa = color[2:-1]
        length = int("0x"+hexa[:-1], 0)
        direction = {
            "0": "R",
            "1": "D",
            "2": "L",
            "3": "U"
        }[hexa[-1]]

        result.append(result[-1] + length * lookup[direction])

    return result


def pairwise(l):
    return zip(l, l[1:])


def calculate_area(path):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    polygon_area = abs(sum(z1.real * z2.imag - z1.imag * z2.real for z1, z2 in pairwise(path)) / 2)
    perimeter_area = sum(abs(z2 - z1) for z1, z2 in pairwise(path))
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # here returning "points inside polygon + points in perimeter"
    return polygon_area + perimeter_area / 2 + 1


def part2():
    path = parse_line_2(data)
    print(calculate_area(path))


part1()
part2()