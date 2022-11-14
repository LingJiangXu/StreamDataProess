# <center>实验lab2
## 题目：
把原本生成的随机数变成二维的$(x_1, x_2, \ldots,x_n)$且$F(X)$、$F(Xn)$具有明显的不同，采用滑动窗口的办法进行聚类，设计一个随机程序来控制所生成的随机数，发生概念漂移，对聚类结果进行比较。
## 求解思路
1. 聚类函数

### 运行逻辑
### 实现细节
- 聚类函数：```k-means```聚类算法。
```python
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
    def euc_dis(x1, x2)

    # 以质心聚类
    def clustering(x_center_set, data_set)
        return cluster

    # 寻找质心
    def find_center(cluster)
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
```