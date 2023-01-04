import random
from matplotlib import pyplot as plt


#k-means聚类
def K_means(data_set, k):
    """
    k-means聚类实现
    :param data_set: 待聚类数据集。点集合，元素为n维数组表示坐标点. ex: [[1,2], [4,6], [18, 19], [16, 19], [-1, -3]] or ([..],[..],...)
    :param k: 待聚类的集合数量. ex: 2
    :return: 聚类后的中心点集合（中心点为n维数组）和以下标为键、聚类点集合列表为值的字典. ex:([[17.0, 19.0], [1.33, 1.66]], {0: [[18, 19], [16, 19]], 1: [[1, 2], [4, 6], [-1, -3]]})
    """

    # 初始值
    global cluster
    data_dim = len(data_set[0])
    center_set = random.sample(data_set, k)

    # 定义欧式距离计算
    def Euc_dis(x1, x2):
        result = [0] * data_dim
        for i in range(data_dim):
            result[i] = (x1[i] - x2[i]) ** 2
        return (sum(result)) ** 0.5

    # 以质心聚类
    def Clustering(x_center_set, data_set):
        cluster = dict(zip([i for i in range(k)], [[] for i in range(k)]))
        for i in data_set:
            distance = [Euc_dis(i, j) for j in x_center_set]
            # i_belong = [j for j in range(k) if distance[j] == min(distance)][0]
            i_belong = distance.index(min(distance))
            cluster[i_belong].append(i)
        return cluster

    # 寻找质心
    def Find_center(cluster):
        finded_center_set = []
        for value_set in cluster.values():
            center_point = [0] * data_dim
            for i in range(data_dim):
                mean = (sum([point[i] for point in value_set])) / len(value_set)
                center_point[i] = mean
                # center_point[i] = np.mean([point[i] for point in value_set])
            finded_center_set.append(center_point)
        return finded_center_set

    # 迭代求解
    epsilon = delta = 0.1  # 迭代阈值epsilon
    while delta >= epsilon:
        old_center = center_set
        cluster = Clustering(center_set, data_set)
        center_set = Find_center(cluster)
        delta = Euc_dis([0] * k, [Euc_dis(x1, x2) for x1, x2 in zip(old_center, center_set)])

    # 返回结果
    return center_set, cluster


# 生成数据
def Generate():
    # 两种正态分布数据
    def Data1():
        return [random.normalvariate(-5, 3)]

    def Data2():
        return [random.normalvariate(10, 2)]

    # 交替生成数据
    generated_data = []
    clu_info = []
    for i in range(999):
        B = [0, 1]
        # 按照0-1分布交替生成两种数据
        if random.choice(B):
            generated_data.append(Data1())
            clu_info.append(0)
        else:
            generated_data.append(Data2())
            clu_info.append(1)

    return generated_data, clu_info

if __name__ == '__main__':
    data, clu_info = Generate()
    # 聚类
    center, clus = K_means(data, 2)
    # clus_points_x = [x[0] for x in clus[0]]+([x[0] for x in clus[1]])  # 被聚类的点（1维）组成的集合
    i, j = 0, 1 if center[0] < center[1] else (1, 0)  # 靠右的分类点定义为0，使其与真实分类一致
    clus_points_y = [i]*len(clus[0]) + [j]*len(clus[1])  # 被聚类点对应的分类
    # 绘制聚类结果
    fig, axs = plt.subplots(2, 1)
    fig.tight_layout()  # 调整子图间距
    axs[0].scatter(data, clu_info, s=1, c=clu_info)
    axs[0].set_title("True classification of data")
    axs[1].scatter(clus[0]+clus[1], clus_points_y, s=1, c=clus_points_y)
    axs[1].set_title("K-neams clustering results")
    plt.show()

