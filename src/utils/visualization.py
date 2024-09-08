import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from src.utils.bench_status import get_benches


def scatter(benches):
    x = []
    y = []
    for bench in benches:
        x.append(float(bench.x))
        y.append(float(bench.y))

    plt.scatter(x, y)
    plt.title('Scatter Plot')
    plt.axis('equal')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()


def line(benches):
    x = []
    y = []
    for bench in benches:
        x.append(float(bench.x))
        y.append(float(bench.y))

    plt.plot(x, y)
    plt.title('Line Plot')
    plt.axis('equal')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()

def serializer(benches):
    x = []
    y = []
    for bench in benches:
        x.append(float(bench.x))
        y.append(float(bench.y))
    return x, y


def rec(rectangles):
    fig, ax = plt.subplots()

    # 遍历每个矩形
    for rect in rectangles:
        # 使用 Polygon 将矩形绘制出来
        polygon = Polygon(rect, closed=True, edgecolor='blue', fill=None)
        ax.add_patch(polygon)

    # 设置轴的范围和比例
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect('equal', adjustable='box')

    # 显示图形
    plt.savefig('rec.png')
    plt.show()


if __name__ == '__main__':
    benches = get_benches(300)
    scatter(benches)