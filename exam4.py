import random
import math
import matplotlib.pyplot as plt


# 由题生成订单数据
def Data():
    # 求解数num的所有小于等于50因数
    def factory(num):
        fac = []
        iter_time = int(math.sqrt(num))
        for i in range(1,iter_time+1):
            if num % i == 0:
                fac.append(i)
                if num / i != i:
                    fac.append(int(num / i))
        return list(filter(lambda x: x<=50, fac))

    return dict(zip( range(1, 101), [factory(num) for num in range(1, 101)] ))

# 黏性抽样算法
def Sticky_sampling(I, idx, X, sigma, epsilon, delta):
    """
    I: 项;
    idx: 项I的到达时序;
    X: 记录集合;
    sigma: 支持度阈值;
    epsilon: 误差阈值;
    delta: 失败概率;
    :return: X: 修改后的记录集合；
    """
    t = (1 / epsilon) * math.log(1 / (sigma * delta))
    r = idx // t + 1  # 采样率
    for c in I:
        if c in X:
            X[c] += 1
        elif random.random() < 1/r:
            X[c] = 1
        else:
            pass

    if (idx != 1) & ((idx-1) % t - idx % t != 0):
        # 当采样率发生变化
        for c in X.copy():
            # 扫描记录集合，“生死考验”
            while True:
                if random.choice([0, 1]):
                    # 运气不错，逃过一劫
                    break
                elif X[c] == 1:
                    # 再减就没了
                    del X[c]
                    break
                else:
                    # unluky but undeath
                    X[c] -= 1

if __name__ == '__main__':
    data = Data()

    # 初始值：
    X_certain = {}
    for idx in range(1, 101):
        I_set = data[idx]
        Sticky_sampling(I_set, idx, X_certain, 4, 0.01, 0.01)

    print(X_certain)
    plt.bar(range(len(X_certain)), X_certain.values())
    plt.xticks(range(len(X_certain)), X_certain.keys())
    plt.title("the result of certian window")
    plt.grid()
    plt.show()










