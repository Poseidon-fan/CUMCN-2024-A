import numpy as np


def get_rectangle_vertices(x0, y0, length, width, k):
    # 计算长边的方向角
    theta = np.arctan(k)

    # 计算长边和宽边方向的单位向量
    dx_length = np.cos(theta)
    dy_length = np.sin(theta)
    dx_width = -dy_length
    dy_width = dx_length

    # 矩形半长和半宽
    half_length = length / 2
    half_width = width / 2

    # 计算四个顶点的坐标
    x1 = x0 + half_length * dx_length + half_width * dx_width
    y1 = y0 + half_length * dy_length + half_width * dy_width

    x2 = x0 + half_length * dx_length - half_width * dx_width
    y2 = y0 + half_length * dy_length - half_width * dy_width

    x3 = x0 - half_length * dx_length - half_width * dx_width
    y3 = y0 - half_length * dy_length - half_width * dy_width

    x4 = x0 - half_length * dx_length + half_width * dx_width
    y4 = y0 - half_length * dy_length + half_width * dy_width

    # 返回四个顶点的坐标
    return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]