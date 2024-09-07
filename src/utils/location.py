import math

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


def get_point_on_circle(center, r, point_A, arc_length, is_shun=False):
    """
    根据圆心、半径、圆上一点A的坐标及弧长，计算圆上另一点B的坐标。

    参数:
    center: 圆心的坐标 (x, y)
    r: 圆的半径
    point_A: 圆上一点A的坐标 (x1, y1)
    arc_length: 从点A到点B的弧长

    返回:
    圆上点B的坐标 (x2, y2)
    """

    # 提取坐标
    cx, cy = center
    x1, y1 = point_A

    # 计算点A相对于圆心的角度
    angle_A = math.atan2(y1 - cy, x1 - cx)

    # 计算弧长对应的圆心角（弧度），公式：θ = 弧长 / 半径
    delta_theta = arc_length / r

    # 计算点B的角度（相对于圆心）
    angle_B = angle_A + delta_theta

    if is_shun:
        angle_B = angle_A - delta_theta

    # 计算点B的坐标
    x2 = cx + r * math.cos(angle_B)
    y2 = cy + r * math.sin(angle_B)

    return (x2, y2)


def locate_turn(r0, theta, t, v):
    x1 = r0 * math.cos(theta)
    y1 = r0 * math.sin(theta)
    x2 = -x1
    y2 = -y1
    c1 = x1, y1
    c2 = -x1, -y1
    c1_r = 2 / 3 * math.sqrt(x1 ** 2 + y1 ** 2)
    c2_r = 1 / 3 * math.sqrt(x1 ** 2 + y1 ** 2)
    c1_center = 4 / 6 * x1 + 2 / 6 * x2, 4 / 6 * y1 + 2 / 6 * y2
    c2_center = 1 / 6 * x1 + 5 / 6 * x2, 1 / 6 * y1 + 5 / 6 * y2
    c2_start = 1/3*x1+2/3*x2, 1/3*y1+2/3*y2
    if (v * t <= math.pi * c1_r):
        return get_point_on_circle(c1_center, c1_r, c1, v * t , is_shun=True)
    elif (v * t > math.pi * c1_r) and (v * t <= math.pi * c1_r + math.pi * c2_r):
        return get_point_on_circle(c2_center, c2_r, c2_start, v * t - math.pi * c1_r, is_shun=False)
    else:
        raise("传入参数长度超过圆周长")


if __name__ == '__main__':
    print(locate_turn(1, math.pi / 2, 2 / 3 * math.pi, 1))


def locate_normal(t, b=0.55, v=1):
    k = b / 2 / np.pi
    theta_0 = 32 * np.pi  # 初始极角为32π
    return position_after_time(k, v, t, theta_0)
