import math

from src.bench import get_benches


def solve():
    location = []
    speed = []
    for t in range(100):
        benches = get_benches(t)
        tmp_location = []
        tmp_speed = []
        for bench in benches:
            if bench.is_valid():
                tmp_location.append([float(bench.x), float(bench.y)])
                tmp_speed.append(float(bench.speed))
            else:
                tmp_location.append(None)
                tmp_speed.append(None)
        location.append(tmp_location)
        speed.append(tmp_speed)
    # 此时 location 和 speed 已经收集到了结果
    return location, speed


if __name__ == '__main__':
    solve()
