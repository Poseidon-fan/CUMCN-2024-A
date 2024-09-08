import math


def polar_curve(theta, b):
    return (b / (2 * math.pi)) * theta

    # 计算曲线在 A 点的切线斜率


def tangent_slope_at_A(theta, b):
    # r = f(θ) 的导数是常数 0.55 / (2π)
    r_prime = b / (2 * math.pi)
    # 切线斜率公式
    numerator = r_prime * math.sin(theta) + polar_curve(theta, b) * math.cos(theta)
    denominator = r_prime * math.cos(theta) - polar_curve(theta, b) * math.sin(theta)
    return numerator / denominator

    # 计算 A 和 A0 之间的斜率


def cos_between_two_slopes(k, k0):
    # print(k,k0)
    numerator = 1 + k * k0
    denominator = math.sqrt(1 + k ** 2) * math.sqrt(1 + k0 ** 2)
    return numerator / denominator


def get_circles(r0, theta):
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
    c2_start = 1 / 3 * x1 + 2 / 3 * x2, 1 / 3 * y1 + 2 / 3 * y2
    return c1, c2, c1_r, c2_r


def get_k(region, theta, dot, r0, theta0, b):
    if region == 1:
        return tangent_slope_at_A(theta, b)
    c1, c2, c1_r, c2_r = get_circles(r0, theta0)
    if region == 2:
        return -(dot[0] - c1[0]) / (dot[1] - c1[1])
    elif region == 3:
        return -(dot[0] - c2[0]) / (dot[1] - c2[1])
    elif region == 4:
        return tangent_slope_at_A(theta - math.pi, b)


def get_speed(theta_1, r1, speed_1, region1, theta_2, r2, region2, r0, theta0, b):
    # print(theta_1, r1, speed_1, region1, theta_2, r2, region2, r0, theta0, b)
    if region2 == 0:
        return 0
    dot1 = r1 * math.cos(theta_1), r1 * math.sin(theta_1)
    dot2 = r2 * math.cos(theta_2), r2 * math.sin(theta_2)
    # print(region2)
    k_A1 = get_k(region1, theta_1, dot1, r0, theta0, b)
    k_A2 = get_k(region2, theta_2, dot2, r0, theta0, b)

    # 计算 AA0 之间的斜率
    k_A1A2 = (dot1[1] - dot2[1]) / (dot1[0] - dot2[0])

    # 计算两条直线之间夹角的正弦值
    cos_A1 = cos_between_two_slopes(k_A1, k_A1A2)
    cos_A2 = cos_between_two_slopes(k_A2, k_A1A2)

    speed_2 = speed_1 * cos_A1 / cos_A2
    return abs(speed_2)


def get_benches_speed(v, benches, r0, theta, b):
    benches[0].speed = v
    for i in range(1, 224):
        benches[i].speed = get_speed(theta_1=benches[i - 1].theta, r1=benches[i - 1].r, speed_1=benches[i - 1].speed,
                                     region1=benches[i - 1].region, theta_2=benches[i].theta, r2=benches[i].r,
                                     region2=benches[i].region, r0=r0, theta0=theta, b=b)
