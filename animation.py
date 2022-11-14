import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm

font = fm.FontProperties(fname="C:\\Windows\\Fonts\\simsun.ttc")  # 设置字体
fig, ax = plt.subplots()
'''
等价于：
fig, ax = plt.add_subplot()
或：
fig = plt.figure()  # 当前画布命名为fig
ax = fig.add_subplot()  # 画布分割，默认1行1列，ax在第一个画布
'''

ax.set_title("动态图", fontproperties=font)
ax.grid(True)
ax.set_xlabel("x轴", fontproperties=font)
ax.set_ylabel("y轴", fontproperties=font)

lines1, = ax.plot([], [], "r--", linewidth=2, label="$\sinx$曲线")
lines2, = ax.plot([], [], "b--", linewidth=2, label="$\cosx$曲线")
ax.legend(loc="upper left", prop=font, shadow=True)

def init():
    # lines1, = ax.plot([], [], "r--", linewidth=2, label="sin曲线")
    # lines2, = ax.plot([], [], "b--", linewidth=2, label="cos曲线")
    return lines1, lines2


def update(frame):
    x = np.linspace(-np.pi + 0.1 * frame, np.pi + 0.1 * frame, 256, endpoint=True)
    y1, y2 = np.sin(x), np.cos(x)

    ax.set_xlim(-4 + 0.1 * frame, 4 + 0.1 * frame)
    ax.set_ylim(-1, 1)
    ax.set_xticks(np.linspace(-4 + 0.1 * frame, 4 + 0.1 * frame, 9, endpoint=True))
    ax.set_yticks(np.linspace(-1, 1, 9))
    ax.figure.canvas.draw() # 更新坐标轴及标题

    lines1, = ax.plot(x, y1, "r--", linewidth=2, label="sin曲线")
    lines2, = ax.plot(x, y2, "b--", linewidth=2, label="cos曲线")

    return lines1, lines2


ani = animation.FuncAnimation(fig, func=update, init_func=init, frames=np.linspace(-5, 5, 5), interval=1000, blit=True)
plt.show()

