import math


class Bench:
    """板凳模型"""
    def __init__(self, length):
        self.length = length  # 两孔间距
        self.r = 0   # 扳手头部极径
        self.theta = 0  # 扳手头极角
        self.x = 0  # 扳手头横坐标
        self.y = 0  # 扳手头纵坐标
        self.speed = 1  # 扳手头部速度
        self.region = 0  # 所属区域  1 2 3 4

    def patch(self, r, theta):
        self.r = r
        self.theta = theta
        self.x = math.cos(theta) * r
        self.y = math.sin(theta) * r

    def __str__(self):
        return '极坐标: [' + str(self.r) + ', ' + str(self.theta) + '] ' + '直角坐标: [' + str(self.x) + ',' + str(self.y) + ']'