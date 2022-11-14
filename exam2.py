import random

import numpy as np


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
        result = [0] * len(x1)
        for i in range(len(x1)):
            result[i] = (x1[i] - x2[i]) ** 2
        return (sum(result)) ** 0.5

    # 以质心聚类
    def clustering(x_center_set, data_set):
        cluster = dict(zip([i for i in range(k)], [[] for i in range(k)]))
        for i in data_set:
            distance = [euc_dis(i, j) for j in x_center_set]
            i_belong = [i for i in range(k) if distance[i] == min(distance)][0]
            cluster[i_belong].append(i)
        return cluster

    # 寻找质心
    def find_center(cluster):
        finded_center_set = []
        for value_set in list(cluster.values()):
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
    data_set = ([12, 2], [3, 4], [5, 6], [8, 9], [-1, -3], [-4, -6], [-2, -4])
    k = 2
    print(k_means(data_set, k))
