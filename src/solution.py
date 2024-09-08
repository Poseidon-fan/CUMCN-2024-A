import math

import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from src.utils.bench_status import get_benches, picture_trace
from src.utils.location import locate_normal
from src.utils.overall_length import overall_length
from src.utils.rec_overlap import is_rectangle_overlap
from src.utils.rec_transform import get_rectangle_vertices
from src.utils.speed import get_benches_speed
from src.utils.visualization import line, serializer, rec, scatter

BENCH_WIDTH = 0.3  # 板凳宽
HEAD_DISTANCE = 0.275  # 孔到头部距离


b = 0.55  # 螺距
benches = []  # 当前状态下，所有板凳的列表


def validate():
    """检测当前状态下的benches是否合法"""
    global benches
    # 先检测第一个
    targets = []  # 记录所有的板凳的坐标
    for i in range(221):  # 这里直接设死了
        cur_bench = benches[i]
        next_bench = benches[i + 1]
        x0 = (cur_bench.x + next_bench.x) / 2
        y0 = (cur_bench.y + next_bench.y) / 2
        length = cur_bench.length + 2 * HEAD_DISTANCE
        width = BENCH_WIDTH
        k = (cur_bench.y - next_bench.y) / (cur_bench.x - next_bench.x)

        targets.append(get_rectangle_vertices(x0, y0, length, width, k))

    for i in range(2, 221):
        # 先检测头
        if is_rectangle_overlap(targets[0], targets[i]):
            return False

    for i in range(3, 221):
        if is_rectangle_overlap(targets[1], targets[i]):
            return False

    return True


def solve1():
    global benches
    speeds = []
    locations = []
    for i in range(301):
        cur_speed = []
        cur_location = []
        benches = get_benches(i)
        get_benches_speed(1, benches, None, None, 0.55)

        for bench in benches:
            if bench.theta > 32 * np.pi:
                cur_location.append(11111)
                cur_location.append(11111)
                cur_speed.append(11111)
            else:
                cur_speed.append(bench.speed)
                cur_location.append(bench.x)
                cur_location.append(bench.y)
        speeds.append(cur_speed)
        locations.append(cur_location)


    df_location = pd.DataFrame(locations).round(6).transpose()
    df_speed = pd.DataFrame(speeds).round(6).transpose()
    df_location.to_excel('res1_locations.xlsx', index=False, header=False)
    df_speed.to_excel('res2_speeds.xlsx', index=False, header=False)

def solve2():
    global benches
    # limits = []
    # for i in np.arange(412, 413, 0.001):
    #     print(i)
    #     benches = get_benches(i)
    #
    #     if not validate():
    #         limits.append(i)
    # print('limits: ', limits)

    # t_limit = limits[0]
    t_limit = 412.4739999999888
    res = []
    benches = get_benches(t_limit)
    get_benches_speed(1, benches, None, None, 0.55)

    scatter(benches)
    line(benches)
    targets = []  # 记录所有的板凳的坐标
    for i in range(222):  # 这里直接设死了
        cur_bench = benches[i]
        next_bench = benches[i + 1]
        x0 = (cur_bench.x + next_bench.x) / 2
        y0 = (cur_bench.y + next_bench.y) / 2
        length = cur_bench.length + 2 * HEAD_DISTANCE
        width = BENCH_WIDTH
        k = (cur_bench.y - next_bench.y) / (cur_bench.x - next_bench.x)

        targets.append(get_rectangle_vertices(x0, y0, length, width, k))

    rec(targets)

    for bench in benches:
        res.append([bench.x, bench.y, bench.speed])
    df = pd.DataFrame(res)
    df.to_excel('res2.xlsx', index=False, header=False)



def solve3():
    global b, benches
    # res = []
    # for b_ in np.arange(0.44, 0.452, 0.0005):
    #     # 遍历螺距
    #     b_ = float(b_)
    #     b = b_
    #     left = 10
    #     right = int(overall_length(b_))
    #     while right - left > 1e-6:
    #         middle = (left + right) / 2
    #         benches = get_benches(middle, b=b_)
    #         if not validate():
    #             right = middle
    #         else:
    #             left = middle
    #     rr = math.sqrt(benches[0].x ** 2 + benches[0].y ** 2)
    #     print('b: ', b, 'r: ', rr)

    left_b = 0.1
    right_b = 0.55
    while right_b - left_b > 1e-6:
        middle_b = (right_b + left_b) / 2

        left_t = 10
        right_t = int(overall_length(middle_b))

        while right_t - left_t > 1e-6:
            middle_t = (right_t + left_t) / 2
            benches = get_benches(middle_t, b=middle_b)
            if validate():
                left_t = middle_t
            else:
                right_t = middle_t


        t_base = (left_t + right_t) / 2
        rr = math.sqrt(benches[0].x ** 2 + benches[0].y ** 2)
        for t in np.arange(t_base - 4.5 * np.pi, t_base, 0.3):
            benches = get_benches(t, b=middle_b)
            if not validate():
                rr = math.sqrt(benches[0].x ** 2 + benches[0].y ** 2)
        print('b: ', middle_b, 'r: ', rr)
        if rr > 4.5:
            left_b = middle_b
        else:
            right_b = middle_b


def solve4():
    global benches, b
    b = 1.7
    v = 1  # 该问中速度恒为1
    t0 = 1333.35  # todo 开始掉头的时刻，当做外层循环变量，后面要循环
    theta_turn, r_turn = locate_normal(t0, b)  # 掉头时刻的极角与极径（掉头圆的半径）
    turning_length = np.pi * r_turn  # 掉头空间内走的路径长度
    turning_time = turning_length / v  # 掉头空间内走的时间
    t_limit = t0 * 2 + turning_time  # 整个龙走出的时间
    cuts = picture_trace(t_limit, t0=t0, b=b, v=v, turning_time=turning_time, theta_turn=theta_turn, r_turn=r_turn)



    # for t in np.arange(t0, t_limit, 0.1):
    #     benches = get_benches(t, t0=t0, b=b, v=v, turning_time=turning_time)
    #     if not validate():
    #         pass

    # for i in np.arange(0, t_limit - 2, 2):
    #     benches = get_benches(i, t0=t0, b=b, v=v, turning_time=turning_time, theta_turn=theta_turn,
    #                           r_turn=r_turn)
    #     cuts.append([benches[0].x, benches[0].y])

    # x_coords = [point[0] for point in cuts]
    # y_coords = [point[1] for point in cuts]
    # # df = pd.DataFrame({
    # #     'x': x_coords,
    # #     'y': y_coords
    # # })
    # # df.to_csv('dot.csv')
    #
    # # 画折线图
    # plt.figure(figsize=(8, 6))
    # plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
    # plt.title("Line Plot of Given Points")
    # plt.xlabel("X Coordinate")
    # plt.ylabel("Y Coordinate")
    # plt.axis('equal')
    # plt.grid(True)
    # plt.show()

    # benches = get_benches(t0 + 2, t0=t0, b=b, v=v, turning_time=turning_time, theta_turn=theta_turn, r_turn=r_turn, cuts=cuts)
    exc = []
    speeds = []
    locations = []
    for i in range(-50, -49):
        print(i)
        try:
            cur_speed = []
            cur_location = []
            benches = get_benches(t0 + i, t0=t0, b=b, v=v, turning_time=turning_time, theta_turn=theta_turn, r_turn=r_turn, cuts=cuts)
            get_benches_speed(v, benches, r_turn, theta_turn, b)

            for bench in benches:
                cur_speed.append(bench.speed)
                cur_location.append(bench.x)
                cur_location.append(bench.y)
            speeds.append(cur_speed)
            locations.append(cur_location)

            targets = []  # 记录所有的板凳的坐标
            for i in range(221):  # 这里直接设死了
                cur_bench = benches[i]
                next_bench = benches[i + 1]
                x0 = (cur_bench.x + next_bench.x) / 2
                y0 = (cur_bench.y + next_bench.y) / 2
                length = cur_bench.length + 2 * HEAD_DISTANCE
                width = BENCH_WIDTH
                k = (cur_bench.y - next_bench.y) / (cur_bench.x - next_bench.x)

                targets.append(get_rectangle_vertices(x0, y0, length, width, k))

            rec(targets)

        except Exception as e:
            print('Wrong!!!', i)
            exc.append(i)
    df_location = pd.DataFrame(locations).round(6).transpose()
    df_speed = pd.DataFrame(speeds).round(6).transpose()
    df_location.to_excel('res4_locations.xlsx', index=False, header=False)
    df_speed.to_excel('res4_speeds.xlsx', index=False, header=False)
    print(exc)


if __name__ == '__main__':
    solve4()

    # benches = get_benches(225)
    # targets = []  # 记录所有的板凳的坐标
    # for i in range(221):  # 这里直接设死了
    #     cur_bench = benches[i]
    #     if cur_bench.theta > 32 * np.pi:
    #         break
    #     next_bench = benches[i + 1]
    #     x0 = (cur_bench.x + next_bench.x) / 2
    #     y0 = (cur_bench.y + next_bench.y) / 2
    #     length = cur_bench.length + 2 * HEAD_DISTANCE
    #     width = BENCH_WIDTH
    #     k = (cur_bench.y - next_bench.y) / (cur_bench.x - next_bench.x)
    #
    #     targets.append(get_rectangle_vertices(x0, y0, length, width, k))
    #
    # rec(targets)