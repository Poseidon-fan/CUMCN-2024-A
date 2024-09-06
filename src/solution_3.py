import math

import src.utils.common as common
from src.bench import get_benches
from src.utils.overall_length import overall_length

benches = []

def validate():
    # 先检测第一个
    first = benches[0]
    for i in range(len(benches)):
        if i > 1 and first.overlap_test(benches[i]):
            return False

    second = benches[1]
    for i in range(len(benches)):
        if i > 2 and second.overlap_test(benches[i]):
            return False

    return True


def margin_radius(b_):
    global benches
    common.b = b_
    left = 10
    right = int(overall_length())
    while right - left > 1e-6:
        middle = (left + right) / 2
        benches = get_benches(middle)
        if validate():
            left = middle
        else:
            right = middle
    return math.sqrt(benches[0].x ** 2 + benches[0].y ** 2)


def solve():
    left = 0.1
    right = 0.55
    while right - left > 1e-6:
        middle = (left + right) / 2
        if margin_radius(middle) < 4.5:
            right = middle
        else:
            left = middle
    print(left)


if __name__ == '__main__':
    solve()

