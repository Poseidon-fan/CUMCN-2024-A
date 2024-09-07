import numpy as np
from scipy.optimize import fsolve


def point_iterate_normal(bench, b):
    """给出板凳头部的孔，以及螺距，求出板凳尾孔的坐标"""
    def equations(theta, x0, y0, r_circle):
        r_spiral = b / (2 * np.pi) * theta
        return r_spiral ** 2 - 2 * x0 * r_spiral * np.cos(theta) - 2 * y0 * r_spiral * np.sin(theta) + x0 ** 2 + y0 ** 2 - r_circle ** 2

    x0 = bench.x
    y0 = bench.y
    r_circle = bench.length
    theta_begin = bench.theta
    theta_range = (theta_begin, theta_begin + np.pi)

    theta_solution = fsolve(equations, np.array([(theta_range[0] + theta_range[1]) / 2]), args=(x0, y0, r_circle))[0]
    r_solution = b / (2 * np.pi) * theta_solution
    return r_solution, theta_solution