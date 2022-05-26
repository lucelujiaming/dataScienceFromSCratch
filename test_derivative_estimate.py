# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import math
import random

# 假设我们拥有某个函数 f，这个函数输入一个实数向量，输出一个实数。一个简单的例子如下：
def sum_of_squares(v):
	"""computes the sum of squared elements in v"""
	return sum(v_i ** 2 for v_i in v)

# 梯度（在微积分里，这表示偏导数向量）给出了输入值的方向
# 导数通过差商的极限来定义：
def difference_quotient(f, x, h):
	return (f(x + h) - f(x)) / h

def square(x):
	return x * x
# 它的导数为：
def derivative(x):
	return 2 * x

# 通过计算一个很小的变动 e 的差商来估算微分。
from functools import partial
derivative_estimate = partial(difference_quotient, square, h=0.00001)
# 绘出导入matplotlib.pyplot作为plt的基本相同的形态
x = range(-10,10)
plt.title("精确的导数值与估计值")
# plt.plot(x, map(derivative, x), 'rx', label='Actual') # 用 x 表示
plt.plot(x, list(map(derivative, x)), 'rx', label='Actual') # 用 x 表示
# plt.plot(x, map(derivative_estimate, x), 'b+', label='Estimate') # 用 + 表示
plt.plot(x, list(map(derivative_estimate, x)), 'b+', label='Estimate') # 用 + 表示
plt.legend(loc=9)
plt.show()
