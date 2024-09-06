import math
import numpy as np
from scipy.optimize import fsolve

import src.utils.common as common

# 定义常量
pi = math.pi
c = common.b / (2 * pi)

# θ2部分的计算结果（之前已经计算好）
theta_2 = 32 * pi
term1_theta2 = (theta_2 / 2) * math.sqrt(theta_2 ** 2 + 1)
term2_theta2 = 0.5 * math.log(theta_2 + math.sqrt(theta_2 ** 2 + 1))
arc_length = c * (term1_theta2 + term2_theta2)

# 使用fsolve求解θ1
def head_locate(t):
    L_target = t
    def arc_length_difference(theta_1):
        theta_1 = theta_1[0]  # 提取数组中的标量值
        term1_theta1 = (theta_1 / 2) * math.sqrt(theta_1 ** 2 + 1)
        term2_theta1 = 0.5 * math.log(theta_1 + math.sqrt(theta_1 ** 2 + 1))

        arc_length_theta1 = c * (term1_theta1 + term2_theta1)
        return (arc_length - arc_length_theta1) - L_target

    return fsolve(arc_length_difference, np.array([0]))[0]
