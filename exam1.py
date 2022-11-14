from time import sleep

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, font_manager
import threading


# 定义储存区类
class Store(object):
    # 初始化对象
    def __init__(self, init_len=20):
        self.len = init_len  # 储存区实例长度
        self.elems = np.array([np.nan] * self.len)  # 储存区实例存储空间
        self.head = 0  # 存储首元素下标
        self.num = 0  # 已存入元素量

    # 判断是否存满
    def is_full(self):
        return self.len == self.num

    # 判断存储区实例是否为空
    def is_empty(self):
        return self.num == 0

    # 去除储存区首元素，若存储区空，则跳过
    def popstore(self):
        if self.is_empty():
            pass
        else:
            self.elems[self.head] = np.nan
            self.head = (self.head + 1) % self.len
            self.num -= 1

    # 查看存储区首元素，若存储区空，返回nan
    def peek(self):
        if self.is_empty():
            return np.nan
        return self.elems[self.head]

    # 向存储区尾部存入元素e，若存储区满，先去除首元素在存
    def enstore(self, e):
        if self.is_full():
            self.popstore()
        self.elems[(self.head + self.num) % self.len] = e
        self.num += 1

    # 查看并去除存储区首元素
    def destore(self):
        e = self.peek()
        self.popstore()
        return e

    # 计算存储区非空元素的均值
    def nanmean(self):
        return np.nanmean(self.elems)


# 写入向存储区元素
def write_data(store):
    write_time = 0  # 写入时间戳，初始为0
    # 不停写入
    while True:
        data_write = np.random.normal(5, 2, 1)  # 写入数据服从正态分布
        write_clock = int(np.random.poisson(6, 1))  # 写入间隔时间服从泊松分布
        store.enstore(data_write)  # 数据写入存储区
        print("{}s，完成数据写入！".format(write_time))  # 打印信息
        write_time += write_clock  # 更新时间戳
        sleep(write_clock)


# 读取储存区的均值
def read_data(store):
    # 定义全局变量，存放读取的数据，方便函数外调用
    global frame_data
    # 读取时间戳， 初始为0
    read_time = 0
    # 不停读取
    while True:
        frame_data = (read_time, store.nanmean())  # 读取的数据，第一项为读取的时间点，第二项为读取内容
        print("{}s，完成数据读取！".format(read_time))  # 打印信息
        read_time += clock  # 更新时间戳
        sleep(clock)


# 读取数据动态可视化
def visualize():
    # 初始画布设置
    font = font_manager.FontProperties(fname="C:\\Windows\\Fonts\\simsun.ttc")  # 字体，兼容中文
    fig, ax = plt.subplots()  # 定义画布
    ax.set_ylim(-5, 14)  # 初始坐标轴区间
    ax.set_xlim(0, 3)
    ax.grid(True)  # 打开网格
    ax.set_title("读取数据的平均值图", fontproperties=font)  # 设置标题
    ax.set_xlabel("时间/s", fontproperties=font)
    ax.set_ylabel("平均值", fontproperties=font)

    x, y = [0], [0]  # 初始点位绘制
    line, = ax.plot(x, y, 'ro-', linewidth=2, label="读取数据均值") # 注意line,为元组，要加逗号
    plt.legend(loc="upper right", prop=font, shadow=True)

    # 初始状态函数
    def init():
        ax.set_xlim(0, 10)
        return line,

    # 更新状态函数
    def update(frame):
        xdata, ydata = frame_data  # 对读取的数据拆包
        x.append(xdata)  # 更新绘制点
        y.append(ydata)
        ymin, ymax = min(y), max(y)

        ax.set_xlim(0, xdata * 4 / 3)  # 更新坐标轴范围
        ax.set_ylim(ymin - 1, ymax * 4 / 3)

        line, = ax.plot(x, y, 'ro-', linewidth=2, label="读取数据均值")  # 绘制更新后的图
        return line,

    # 调用动态绘图函数并显示
    ani = animation.FuncAnimation(fig=fig, init_func=init, func=update, frames=1, interval=clock * 1000, blit=False)   # interval为更新图像时间间隔，单位ms
    plt.show()


if __name__ == '__main__':
    # 初始化
    frame_data = (0, 0)  # 初始读取数据时间与内容为0
    clock = 6  # 读取以及绘图周期为6s
    store = Store(30)  # 实例化存储区，空间为30

    # 双线程执行写入与读取任务
    write_task = threading.Thread(target=write_data, args=(store,), daemon=True)  # daemon设置主线程守护
    read_task = threading.Thread(target=read_data, args=(store,), daemon=True)
    write_task.start()
    read_task.start()

    # 动态可视化，若没有此行，则主线程到此结束，所有线程跟着结束
    visualize()

