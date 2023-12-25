from itertools import combinations
import cmath


def get_points(input_file):
    return [(complex(int(y[0]), int(y[1])), complex(int(y[4]), int(y[5]))) for y in [x.replace(",", "").split() for x in open(input_file).read().splitlines()]]


def in_limits(z,  x_limits, y_limits):
    return (x_limits[0] <= z.real < x_limits[1] ) and (y_limits[0] <= z.imag < y_limits[1])


def collision_times(z1, dz1, z2, dz2):
    t1 = 1 / (dz2.imag / dz2.real * dz1.real - dz1.imag) * (z1.imag - z2.imag - dz2.imag / dz2.real * (z1.real - z2.real))
    t2 =  1 / dz2.real * (z1.real - z2.real + t1 * dz1.real)
    return t1, t2 


def is_parallel(dz1, dz2):
    return cmath.phase(dz1) == cmath.phase(dz2) or cmath.phase(dz1) == cmath.phase(-dz2)


def future_intersections(points, x_limits, y_limits):
    ret = 0

    for (x, dx), (y, dy) in combinations(points, 2):
        if not is_parallel(dx, dy):
            t1, t2 = collision_times(x, dx, y, dy)
            if not (t1 < 0 or t2 < 0):
                c = x + t1 * dx 
                if in_limits(c, x_limits, y_limits):
                    ret += 1
    return ret


def test_part_1():
    points = get_points("toy")
    assert future_intersections(points, (7, 27), (7, 27)) == 2


def part1():
    points = get_points("real")
    return future_intersections(points, (200000000000000, 400000000000001), (200000000000000, 400000000000001))


test_part_1()
print(part1())


