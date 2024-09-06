"""
判断两个矩形是否有重叠部分
"""

import numpy as np


def vector_projection(v1, v2):
    """返回v1在v2上的投影"""
    return np.dot(v1, v2) / np.linalg.norm(v2) ** 2 * v2


def interval_overlap(proj1, proj2):
    """判断两个投影区间是否重叠"""
    return not (max(proj1) < min(proj2) or max(proj2) < min(proj1))


def get_axes(rect):
    """获取矩形的分离轴（即边的法向量）"""
    axes = []
    for i in range(4):
        p1 = rect[i]
        p2 = rect[(i + 1) % 4]
        edge = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        normal = np.array([-edge[1], edge[0]])  # 计算边的法向量
        axes.append(normal)
    return axes


def project_rectangle(rect, axis):
    """将矩形投影到给定的轴上"""
    projections = []
    for vertex in rect:
        projection = np.dot(vertex, axis) / np.linalg.norm(axis)
        projections.append(projection)
    return [min(projections), max(projections)]


def is_rectangle_overlap(rect1, rect2):
    # 获取两个矩形的所有分离轴
    axes1 = get_axes(rect1)
    axes2 = get_axes(rect2)

    # 检查每个轴上的投影是否有重叠
    for axis in axes1 + axes2:
        proj1 = project_rectangle(rect1, axis)
        proj2 = project_rectangle(rect2, axis)
        if not interval_overlap(proj1, proj2):
            return False

    return True


if __name__ == '__main__':
    rect1 = [[7.34585308, 0.58483559], [6.30703264, 3.89044856], [6.02083239, 3.8005074 ], [7.05965282, 0.49489443]]
    rect2 = [(3, 2), (5, 5), (7, 3), (5, 0)]
    if is_rectangle_overlap(rect1, rect2):
        print('yes')
    else:
        print('no')
