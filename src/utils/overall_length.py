import numpy as np
from scipy.integrate import quad

import src.utils.common as common


def overall_length():
    k = common.b / 2 / np.pi
    def integrand(theta):
        return np.sqrt((k * theta) ** 2 + k ** 2)

    # 使用数值积分计算曲线长度
    length, _ = quad(integrand, 0, 32 * np.pi)
    return length



