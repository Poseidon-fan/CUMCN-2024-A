import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 假设这是你封装的函数，用于生成折线图数据
def my_line(n):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + n / 10.0)  # 根据传入的整数n变化生成不同的曲线
    return x, y

# 创建画布
fig, ax = plt.subplots()
xdata, ydata = my_line(0)  # 初始化时的曲线
line, = ax.plot(xdata, ydata)

# 更新函数，用于更新折线图
def update(frame):
    x, y = my_line(frame)
    line.set_data(x, y)
    return line,

# 创建动画，frames表示整数从0到100，interval表示每帧之间的间隔时间（毫秒）
ani = FuncAnimation(fig, update, frames=range(100), interval=100, blit=True)

# 显示动画
plt.show()  # 这行会启动动画显示
