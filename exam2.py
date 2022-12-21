import random
import threading
from time import sleep

import numpy as np
import matplotlib.pyplot as plt

# 数据库类
class DataStore():
    def __init__(self, volum=50):
        self.volum = volum  # 存储容量
        self.elems = []  # 实例空间
        self.nums = 0  # 已存储元素量
        print("INFO: 成功创建数据库实例")

    def __isfull(self):
        '''判断是否满'''
        return self.nums == self.volum

    def enStore(self, ele):
        '''存入元素'''
        if self.__isfull():
            return
        self.elems.append(ele)
        self.nums += 1

    def deStore(self, start, end):
        '''读取元素'''
        if start < self.nums:
            return [self.elems[i] for i in range(start, min(self.nums, end))]
            # return self.elems[start, end] if end <= self.nums else self.elems[start, self.nums]
        else:
            return None

# 写入函数
def write_data(store):
    def Data1():
        '''符合特征1的二维数据'''
        dta1 = random.randrange(-25, 25)
        dta2 = -dta1 + 25 + random.randrange(-5, 5)
        return dta1, dta2

    def Data2():
        '''符合特征2的二维数据'''
        dta1 = random.randrange(-25, 25)
        dta2 = -dta1 - 25 + random.randrange(-5, 5)
        return dta1, dta2

    def Data3():
        '''符合特征3的二维数据，此处用作概念漂移'''
        dta1 = random.randrange(-25, 25)
        dta2 = dta1 + 1 + random.randrange(-10, 8)
        return dta1, dta2

    while True:
        k = random.choices((1, 2, 3), weights=[4, 4, 1], k=1)
        wdata = eval("Data{}()".format(k[0]))
        store.enStore(wdata)
        wait = np.random.poisson(3, 1)
        print("INFO: 写入{},{}数据成功，等待{}s继续写入！".format(k, wdata, wait[0]))
        sleep(wait[0])

# 读取及可视化函数
def read_data(store):

    def draw(ax, center, points):
        '''将聚类结果可视化，聚类中心用18号星号表示，聚类点用14号实心圆表示'''
        plt.xlim(-45, 45)
        plt.ylim(-50, 50)
        plt.axvline(0)
        plt.axhline(0)
        ax.scatter(center[0][0], center[0][1], s=18, c="r", marker='*')
        ax.scatter(center[1][0], center[1][1], s=18, c="g", marker='*')
        ax.scatter([x[0] for x in points[0]], [y[1] for y in points[0]], s=14, c="r", marker='o')
        ax.scatter([x[0] for x in points[1]], [y[1] for y in points[1]], s=14, c="g", marker='o')

    window = 12
    start = 0
    # global rdata
    while True:
        sleep(3)
        start += 1
        rdata = store.deStore(start, start + window)
        if rdata:
            print("INFO: 读取数据成功！为{}".format(rdata))
            poi, clus = k_means(rdata, 2)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            draw(ax, poi, clus)
            plt.pause(2)
            print("INFO: 读取数据聚类并可视化成功！")
        else:
            print("INFO: 读取pass！")
            continue

# k-means聚类
def k_means(data_set, k):
    """
    k-means聚类实现
    :param data_set: 待聚类数据集。点集合，元素为n维数组表示坐标点
    :param k: 待聚类的集合数量
    :return: 聚类后的中心点和以下标键，聚类点集列表维值的字典
    """

    # 初始值
    data_dim = len(data_set[0])
    center_set = random.sample(data_set, k)

    # 定义欧式距离计算
    def euc_dis(x1, x2):
        result = [0] * data_dim
        for i in range(data_dim):
            result[i] = (x1[i] - x2[i]) ** 2
        return (sum(result)) ** 0.5

    # 以质心聚类
    def clustering(x_center_set, data_set):
        cluster = dict(zip([i for i in range(k)], [[] for i in range(k)]))
        for i in data_set:
            distance = [euc_dis(i, j) for j in x_center_set]
            # i_belong = [j for j in range(k) if distance[j] == min(distance)][0]
            i_belong = distance.index(min(distance))
            cluster[i_belong].append(i)
        return cluster

    # 寻找质心
    def find_center(cluster):
        finded_center_set = []
        for value_set in cluster.values():
            center_point = [0] * data_dim
            for i in range(data_dim):
                center_point[i] = np.mean([j[i] for j in value_set])
            finded_center_set.append(center_point)
        return finded_center_set

    # 迭代求解
    epsilon = delta = 0.1  # 迭代阈值epsilon
    while delta >= epsilon:
        old_center = center_set
        cluster = clustering(center_set, data_set)
        center_set = find_center(cluster)
        delta = euc_dis([0] * k, [euc_dis(x1, x2) for x1, x2 in zip(old_center, center_set)])

    # 返回结果
    return center_set, cluster


if __name__ == '__main__':
    # 实例化数据库并设置任务线程
    store = DataStore()
    write_task = threading.Thread(target=write_data, args=(store,), daemon=True)

    # 启动线程
    write_task.start()
    sleep(30)
    read_data(store)

