import numpy as np
from scipy.optimize import fsolve

from .common import b


def equations(theta, x0, y0, len_):
    # 螺线的极坐标方程
    r_spiral = b / (2 * np.pi) * theta

    return r_spiral ** 2 - 2 * x0 * r_spiral * np.cos(theta) - 2 * y0 * r_spiral * np.sin(theta) + x0 ** 2 + y0 ** 2 - len_ ** 2


def point_iterate(bench):
    x0 = bench.x
    y0 = bench.y
    len_ = bench.length
    theta0 = bench.theta
    theta_range = (theta0, theta0 + np.pi)

    theta_solution = fsolve(equations, np.array([(theta_range[0] + theta_range[1]) / 2]), args=(x0, y0, len_))[0]
    r_solution = b / (2 * np.pi) * theta_solution

    return r_solution, theta_solution

    # 返回构造出来的结点
    # bench_next = Bench(len_)
    # bench_next.patch(r_solution, theta_solution)
    # return bench_next


