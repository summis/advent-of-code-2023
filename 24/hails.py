from itertools import combinations
import cmath
from scipy import linalg



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


def get_points_2(input_file):
    return [((int(y[0]), int(y[1]), int(y[2])), (int(y[4]), int(y[5]), int(y[6]))) for y in [x.replace(",", "").split() for x in open(input_file).read().splitlines()]]


def solve_problem(input_type):
    points = get_points_2(input_type)

    w1, dw1 = points[0]
    w2, dw2 = points[1]
    w3, dw3 = points[2]

    A, C = calculate_coefficients(w1, dw1, w2, dw2, w3, dw3)

    x, dx, y, dy, z, dz = linalg.solve(A, C)

    return (x, y, z), (dx, dy, dz)


def part2():
    p, dp = solve_problem("real")
    return sum(p)


def calculate_coefficients(w1, dw1, w2, dw2, w3, dw3):
    # Basic idea:
    # x + dx t = z + dz t 
    # where t = time when hails collide
    #
    # x is unknown starting point, dx unknown speed, z is any know starting position of any hail, dz its speed
    #
    # Solve for t
    #
    # Arrance all nonlinear terms to left side, move all other to right hand side
    # Do same thing for another point z'
    # Equate nonlinear terms, they stay constant
    #
    # Linear system, profit

    A = []
    C = []

    # y dx - x dy
    def _get_part_1(w, dw):
        return (-dw[1], w[1], dw[0], -w[0], 0, 0), -w[1] * dw[0] + dw[1] * w[0]
    
    # z dx - x dz
    def _get_part_2(w, dw):
        return (-dw[2], w[2], 0, 0, dw[0], -w[0]), -w[2] * dw[0] + dw[2] * w[0]
    
    # z dy - y dz
    def _get_part_3(w, dw):
        return (0, 0, -dw[2], w[2], dw[1], -w[1]), -w[2] * dw[1] + dw[2] * w[1]

    for (z1, dz1), (z2, dz2) in (((w1, dw1), (w2, dw2)), ((w1, dw1), (w3, dw3))):
        for coef_function in (_get_part_1, _get_part_2, _get_part_3):
            a1, c1 = coef_function(z1, dz1)
            a2, c2 = coef_function(z2, dz2)

            A.append(
                [(x - y) for x, y in zip(a1, a2)]
            )
            C.append(-(c1 - c2)) # Extra minus to consider flipping of signs when arrancing sides to standard format Ax = C

    return A, C


test_part_1()

print(part1(), part2())


