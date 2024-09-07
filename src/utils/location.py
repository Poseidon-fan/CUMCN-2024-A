import numpy as np
from scipy.integrate import quad


# 定义计算弧长微分函数
def arc_length_integral(theta, k):
    return np.sqrt(k ** 2 + (k * theta) ** 2)


# 定义计算位置函数
def position_after_time(k, v, t, theta_0):
    # 计算初始弧长
    initial_arc_length, _ = quad(arc_length_integral, 0, theta_0, args=(k,))

    # 目标弧长
    target_arc_length = initial_arc_length - v * t  # 这里是沿着极角减小的方向运动

    # 定义通过弧长反求theta的函数
    def find_theta_for_arc_length(theta, k, target_arc_length):
        arc_length, _ = quad(arc_length_integral, 0, theta, args=(k,))
        return arc_length - target_arc_length

    # 使用数值方法求解目标弧长对应的theta
    from scipy.optimize import fsolve
    theta_t = fsolve(find_theta_for_arc_length, theta_0, args=(k, target_arc_length))[0]

    # 计算对应的极径r(t)
    r_t = k * theta_t

    return theta_t, r_t


def locate(t, b=0.55, v=1):
    k = b / 2 / np.pi
    theta_0 = 32 * np.pi  # 初始极角为32π
    return position_after_time(k, v, t, theta_0)
