import math

from src.Bench import Bench
from src.utils.location import locate_normal, locate_turn
from src.utils.point_iteration import point_iterate_normal, point_iterate_turn


def get_benches_normal(t, b, v):
    benches = []
    first = Bench(2.86)
    head_theta, head_r = locate_normal(t, b, v)
    first.patch(head_r, head_theta)
    benches.append(first)

    cur_bench = first
    for i in range(222):
        next_bench = Bench(1.65)
        next_bench.patch(*point_iterate_normal(cur_bench, b))
        benches.append(next_bench)
        cur_bench = next_bench

    for bench in benches:
        bench.region = 1

    return benches


def get_benches_turn(t, t0, b, v, turning_time, theta_turn, r_turn):
    benches = []
    first = Bench(2.86)
    if t > t0 + turning_time:
        # 头已经走出了掉头区域
        head_theta_reverse, head_r_reverse = locate_normal(2 * t0 + turning_time - t, b, v)
        first.patch(head_r_reverse, -head_theta_reverse)
    else:
        head_x, head_y = locate_turn(r_turn, theta_turn, t, v)
        first.patch(math.sqrt(head_x ** 2 + head_y ** 2), math.atan2(head_y, head_x))
    benches.append(first)
    cur_bench = first

    for i in range(222):
        next_bench = Bench(1.65)
        iter_res = point_iterate_turn(cur_bench, b, r_turn, theta_turn)
        next_bench.patch(*iter_res[0])
        next_bench.region = iter_res[1]
        benches.append(next_bench)
        cur_bench = next_bench
    return benches


def get_benches(t, t0=100000, b=0.55, v=1, turning_time=None, theta_turn=None, r_turn=None):
    """
    获取 t 时刻的板凳状态
    t0 为设定的截止时刻，代表开始掉头
    b 为当前设定的螺距
    v 为龙头的速度
    """
    if t <= t0:
        return get_benches_normal(t, b, v)
    else:
        return get_benches_turn(t, t0, b, v, turning_time, theta_turn, r_turn)
