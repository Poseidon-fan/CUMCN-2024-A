import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    benches = get_benches(300)
    scatter(benches)