import math


def get_speed(theta_1, theta_2, speed_1):
    def polar_curve(theta):
        return (0.55 / (2 * math.pi)) * theta

    # 计算曲线在 A 点的切线斜率
    def tangent_slope_at_A(theta):
        # r = f(θ) 的导数是常数 0.55 / (2π)
        r_prime = 0.55 / (2 * math.pi)
        # 切线斜率公式
        numerator = r_prime * math.sin(theta) + polar_curve(theta) * math.cos(theta)
        denominator = r_prime * math.cos(theta) - polar_curve(theta) * math.sin(theta)
        return numerator / denominator

    # 计算 A 和 A0 之间的斜率
    def slope_between_A_A0(theta, theta0):
        r_A = polar_curve(theta)
        r_A0 = polar_curve(theta0)

        x_A = r_A * math.cos(theta)
        y_A = r_A * math.sin(theta)

        x_A0 = r_A0 * math.cos(theta0)
        y_A0 = r_A0 * math.sin(theta0)

        return (y_A - y_A0) / (x_A - x_A0)

    # 计算两条直线之间的夹角的正弦值
    def cos_between_two_slopes(k, k0):
        numerator = 1 + k * k0
        denominator = math.sqrt(1 + k ** 2) * math.sqrt(1 + k0 ** 2)
        return numerator / denominator

    # 计算 A 点处的切线斜率
    k_A1 = tangent_slope_at_A(theta_1)
    k_A2 = tangent_slope_at_A(theta_2)

    # 计算 AA0 之间的斜率
    k_A1A2 = slope_between_A_A0(theta_1, theta_2)

    # 计算两条直线之间夹角的正弦值
    cos_A1 = cos_between_two_slopes(k_A1, k_A1A2)
    cos_A2 = cos_between_two_slopes(k_A2, k_A1A2)

    speed_2 = speed_1 * cos_A1 / cos_A2
    return speed_2