# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import math
import random
from collections import Counter # 默认未加载

# 标准正态分布用函数math.erf 描述：
def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

# 举一个易于理解的验证例子——带有 n 和 p 两个参数的二项式随机变量。
# 每个伯努利随机变量等于 1 的概率是 p，等于 0 的概率是 1-p：
def bernoulli_trial(p):
    return 1 if random.random() < p else 0
# 一个二项式随机变量 Binonimal(n,p) 是 n 个独立伯努利随机变量 Bernoulli(p) 之和，
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))

# 把两个分布都在图上绘出来，很容易看出相似性：
def make_hist(p, n, num_points):
    data = [binomial(n, p) for _ in range(num_points)]
    # 用条形图绘出实际的二项式样本
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
        [v / num_points for v in histogram.values()],
        0.8,
        color='0.75')
    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))
    # 用线形图绘出正态近似
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - 
          normal_cdf(i - 0.5, mu, sigma)
                for i in xs]
    plt.plot(xs,ys)
    plt.title("二项分布与正态近似")
    plt.show()

make_hist(0.75, 100, 10000)
