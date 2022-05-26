# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import math
import random
from inverse_normal_cdf import *

from collections import Counter # 默认未加载
def bucketize(point, bucket_size):
    """floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)
def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)
def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()

random.seed(0)
# -100到100之间均匀抽取
uniform = [200 * random.random() - 100 for _ in range(10000)]
# 均值为0标准差为57的正态分布
normal = [57 * inverse_normal_cdf(random.random())
 for _ in range(10000)]

# 展示均匀分布。
plot_histogram(uniform, 10, "均匀分布的直方图")
# 展示了正态分布：
plot_histogram(normal, 10, "正态分布的直方图")
