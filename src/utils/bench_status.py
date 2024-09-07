from src.Bench import Bench
from src.utils.location import locate
from src.utils.point_iteration import point_iterate_normal


def get_benches_normal(t, b, v):
    benches = []
    first = Bench(2.86)
    head_theta, head_r = locate(t, b, v)
    first.patch(head_r, head_theta)
    benches.append(first)

    cur_bench = first
    for i in range(222):
        next_bench = Bench(1.65)
        next_bench.patch(*point_iterate_normal(cur_bench, b))
        benches.append(next_bench)
        cur_bench = next_bench

    return benches

def get_benches_turn(t, t0, b, v):
    pass


def get_benches(t, t0=100000, b=0.55, v=1):
    """
    获取 t 时刻的板凳状态
    t0 为设定的截止时刻，代表开始掉头
    b 为当前设定的螺距
    v 为龙头的速度
    """
    if t <= t0:
        return get_benches_normal(t, b, v)
    else:
        return get_benches_turn(t, t0, b, v)
