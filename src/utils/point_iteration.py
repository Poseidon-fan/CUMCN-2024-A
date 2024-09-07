import math

import numpy as np
from scipy.optimize import fsolve


def judge_theta_interval(x1, y1, x2, y2):

    # 计算叉积
    cross_product = x1 * y2 - y1 * x2

    # 判断theta的区间
    if cross_product > 0:
        return True  # 逆时针
    elif cross_product < 0:
        return False  # 顺时针
    else:
        # 叉积为0时，说明向量共线，需要进一步判断是否同向或反向
        dot_product = x1 * x2 + y1 * y2
        if dot_product > 0:
            return False
        else:
            return True


def point_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def judge_point(cuts, candidates):
    """给定一些候选的点，判断哪个是正确的（根据时间先后性）"""
    overall = []  # 候选点与该点的目标点的集合
    for candidate in candidates:
        target_point = cuts[0]
        target_distance = point_distance(candidate[0], candidate[1], target_point[0], target_point[1])
        for cut in cuts:
            new_distance = point_distance(candidate[0], candidate[1], cut[0], cut[1])
            if new_distance < target_distance:
                target_point = cut
                target_distance = new_distance
        overall.append([candidate, target_point])
    tar = min(overall, key=lambda x: x[1][3])
    # print('candidates: ', candidates)
    return tar[0]



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


def handle_region_4(bench, b):
    """处理区域四"""
    def equations(theta, x0, y0, r_circle):
        r_spiral = b / (2 * np.pi) * (theta - np.pi)
        return r_spiral ** 2 - 2 * x0 * r_spiral * np.cos(theta) - 2 * y0 * r_spiral * np.sin(theta) + x0 ** 2 + y0 ** 2 - r_circle ** 2

    x0 = bench.x
    y0 = bench.y
    r_circle = bench.length
    theta_begin = bench.theta
    theta_range = (theta_begin - np.pi, theta_begin)

    theta_solution = fsolve(equations, np.array([(theta_range[0] + theta_range[1]) / 2]), args=(x0, y0, r_circle))[0]
    r_solution = b / (2 * np.pi) * (theta_solution - np.pi)
    return r_solution, theta_solution


# 极坐标转直角坐标函数
def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def find_circle_intersections(x1, y1, r1, x2, y2, r2):
    # 计算圆心距离
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # 如果圆不相交或一个圆包含另一个圆，则返回空结果
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return None

    # 计算交点
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)

    x0 = x1 + a * (x2 - x1) / d
    y0 = y1 + a * (y2 - y1) / d

    # 交点1
    x3 = x0 + h * (y2 - y1) / d
    y3 = y0 - h * (x2 - x1) / d

    # 交点2
    x4 = x0 - h * (y2 - y1) / d
    y4 = y0 + h * (x2 - x1) / d

    if x3 - x4 < 12 - 10 and y3 - y4 < 1e-10:
        return (x3, y3),
    return (x3, y3), (x4, y4)


def handle_region_2_3(which_circle, r0, x1, y1, r1):
    """
    :param which_circle: 区域2/3
    :param r0: 掉头区域大小，小于4.5
    :param x1: 圆心x
    :param y1: 圆心y
    :param r1: 圆半径
    :return: 解的xy坐标
    """
    if which_circle == 2:
        r2, theta2, R2 = r0 / 3, 2 * np.pi * r0 / 1.7, 2 * r0 / 3
    else:
        r2, theta2, R2 = 2 * r0 / 3, np.pi + 2 * np.pi * r0 / 1.7, r0 / 3
    x2, y2 = polar_to_cartesian(r2, theta2)

    # 定义两个圆的方程
    return find_circle_intersections(x1, y1, r1, x2, y2, R2)



def check_circle_intersection(x1, y1, r1, x2, y2, r2):
    # 计算两个圆心之间的距离
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # 判断两个圆的相对位置
    if d > r1 + r2:
        return False  # 两个圆相离，没有交点
    elif r1 - r2 < d < r1 + r2:
        return True  # 两个圆相交，有两个交点
    elif d == r1 + r2 or d == abs(r1 - r2):
        return True  # 两个圆外切或内切，有一个交点
    elif d < abs(r1 - r2):
        return False  # 一个圆包含另一个圆，没有交点
    else:
        return False  # 未知情况，通常不会出现


def point_iterate_turn(bench, b, break_point_r, break_point_theta, cuts):
    """
    :param cuts: 散点
    :param bench: 板凳头
    :param b: 螺距
    :param break_point_r: 转换点的极径
    :param break_point_theta: 转换点的极角
    """

    # 转换点的直角坐标
    break_point_x = break_point_r * math.cos(break_point_theta)
    break_point_y = break_point_r * math.sin(break_point_theta)

    # 区域二、三圆心的位置
    circle_center_2_x = break_point_r / 3 * math.cos(break_point_theta)
    circle_center_2_y = break_point_r / 3 * math.sin(break_point_theta)
    circle_center_3_x = -break_point_r * 2 / 3 * math.cos(break_point_theta)
    circle_center_3_y = -break_point_r * 2 / 3 * math.sin(break_point_theta)

    valid_1 = bench.region <= 2

    valid_2 = (bench.region == 2 or bench.region == 3) and check_circle_intersection(circle_center_2_x, circle_center_2_y, break_point_r * 2 / 3, bench.x, bench.y, bench.length)

    valid_3 = bench.region >= 3 and check_circle_intersection(circle_center_3_x, circle_center_3_y, break_point_r / 3, bench.x, bench.y, bench.length)

    valid_4 = bench.region == 4

    # if valid_4:
    #     return handle_region_4(bench, b), 4
    # if valid_3:
    #     res = handle_region_2_3(3, break_point_r, bench.x, bench.y, bench.length)
    #     if judge_theta_interval(break_point_x, break_point_y, res[0][0] - circle_center_3_x, res[0][1] - circle_center_3_y):
    #         return (math.sqrt(res[0][0] ** 2 + res[0][1] ** 2), np.atan2(res[0][1], res[0][0])), 3
    #     elif judge_theta_interval(break_point_x, break_point_y, res[1][0] - circle_center_3_x, res[1][1] - circle_center_3_y):
    #         return (math.sqrt(res[1][0] ** 2 + res[1][1] ** 2), np.atan2(res[1][1], res[1][0])), 3
    #     else:
    #         raise ('非法的3区域')
    # elif valid_2:
    #     res = handle_region_2_3(2, break_point_r, bench.x, bench.y, bench.length)
    #     if judge_theta_interval(break_point_x, break_point_y, res[0][0] - circle_center_2_x,
    #                             res[0][1] - circle_center_2_y):
    #         return (math.sqrt(res[0][0] ** 2 + res[0][1] ** 2), np.atan2(res[0][1], res[0][0])), 2
    #     elif judge_theta_interval(break_point_x, break_point_y, res[1][0] - circle_center_2_x,
    #                               res[1][1] - circle_center_2_y):
    #         return (math.sqrt(res[1][0] ** 2 + res[1][1] ** 2), np.atan2(res[1][1], res[1][0])), 2
    #     else:
    #         raise ('非法的2区域')
    # elif valid_4:
    #     return handle_region_4(bench, b), 4
    # else:
    #     return point_iterate_normal(bench, b), 1
    candidates = []
    if valid_4:
        r, theta = handle_region_4(bench, b)
        candidates.append([r * math.cos(float(theta)), r * math.sin(float(theta)), 4])
    if valid_3:
        res = handle_region_2_3(3, break_point_r, bench.x, bench.y, bench.length)
        if res and judge_theta_interval(break_point_x, break_point_y, res[0][0] - circle_center_3_x, res[0][1] - circle_center_3_y):
            candidates.append([res[0][0], res[0][1], 3])
        if res and len(res) >= 2 and judge_theta_interval(break_point_x, break_point_y, res[1][0] - circle_center_3_x, res[1][1] - circle_center_3_y):
            candidates.append([res[1][0], res[1][1], 3])
    if valid_2:
        res = handle_region_2_3(2, break_point_r, bench.x, bench.y, bench.length)
        if res and judge_theta_interval(break_point_x, break_point_y, res[0][0] - circle_center_2_x, res[0][1] - circle_center_2_y):
            candidates.append([res[0][0], res[0][1], 2])
        if res and len(res) >= 2 and judge_theta_interval(break_point_x, break_point_y, res[1][0] - circle_center_2_x, res[1][1] - circle_center_2_y):
            candidates.append([res[1][0], res[1][1], 2])

    if valid_1:
        r, theta = point_iterate_normal(bench, b)
        candidates.append([r * math.cos(float(theta)), r * math.sin(float(theta)), 1])

    tar = judge_point(cuts, candidates)
    return (math.sqrt(float(tar[0]) ** 2 + float(tar[1]) ** 2 ), np.atan2(float(tar[1]), float(tar[0]))), tar[2]


if __name__ == '__main__':
    print(judge_theta_interval(1, 1, -1, 1))
