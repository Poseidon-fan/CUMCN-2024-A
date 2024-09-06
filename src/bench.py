import math

import numpy as np

from src.utils.common import over_length, bench_width, b
from src.utils.locate import head_locate
from src.utils.point_iterate import point_iterate
from src.utils.rec_overlap import is_rectangle_overlap


class Bench:
    """板凳头模型"""
    def __init__(self, length):
        self.length = length
        self.r = 0  # 头部的半径
        self.theta = 0  # 头部的极角
        self.x = 0  # 头部的x坐标
        self.y = 0  # 头部的y坐标

    def __str__(self):
        return '极坐标: [' + str(self.r) + ', ' + str(self.theta) + '] ' + '直角坐标: [' + str(self.x) + ',' + str(self.y) + ']'

    def distance(self, bench):
        """
        计算两个板凳头的距离，用于校验
        """
        return math.sqrt((self.x - bench.x) ** 2 + (self.y - bench.y) ** 2)

    def next(self, length):
        """板凳尾（下一个板凳头）"""
        r, theta = point_iterate(self)
        next_bench = Bench(length)
        next_bench.patch(r, theta)
        return next_bench

    def rec_transform(self):
        """变换为矩形顶点坐标"""
        tail = self.next(self.length)

        # 中心点坐标
        x0 = (self.x + tail.x) / 2
        y0 = (self.y + tail.y) / 2
        length = self.length + 2 * over_length
        width = bench_width
        k = (tail.y - self.y) / (tail.x - self.x)  # 长方向的斜率

        # 计算长边和宽边的角度
        theta = np.arctan(k)

        # 矩形的半长和半宽
        half_length = length / 2
        half_width = width / 2

        # 旋转矩阵
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta), np.cos(theta)]])

        # 矩形未旋转时的四个顶点相对于中心点的坐标
        vertices = np.array([[half_length, half_width],
                             [-half_length, half_width],
                             [-half_length, -half_width],
                             [half_length, -half_width]])

        # 旋转后的顶点坐标
        rotated_vertices = vertices.dot(rotation_matrix.T)

        # 将顶点平移到中心点的坐标位置
        rotated_vertices[:, 0] += x0
        rotated_vertices[:, 1] += y0

        return rotated_vertices

    def patch(self, r, theta):
        """指派坐标"""
        self.r = r
        self.theta = theta
        self.x = math.cos(theta) * r
        self.y = math.sin(theta) * r

    def overlap_test(self, bench):
        """碰撞检测"""
        return is_rectangle_overlap(self.rec_transform(), bench.rec_transform())

    def locate(self, t):
        """定位方法"""
        theta = head_locate(t)
        r = b / (2 * np.pi) * theta
        self.patch(r, theta)

    def is_valid(self):
        return self.theta <= 2 * math.pi * 16

def get_benches(t):
    benches = []
    first = Bench(2.86)
    first.locate(t)

    benches.append(first)
    cur_bench = first

    for i in range(222):
        next_bench = cur_bench.next(1.65)
        benches.append(next_bench)
        cur_bench = next_bench
    return benches


if __name__ == '__main__':
    bench = Bench(2.86)
    bench.patch(8.699964553170402, 99.38816264266087)
    print(bench.next(bench.length).distance(bench.next(bench.length).next(bench.length)))  # 2.86
    print(bench.overlap_test(bench))