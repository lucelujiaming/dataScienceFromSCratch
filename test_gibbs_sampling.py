# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *
from my_cluster import *

import math
import random, re
from collections import defaultdict

# 通过下列代码来轻松生成掷两只骰子所需样本：
def roll_a_die():
	return random.choice([1,2,3,4,5,6])
def direct_sample():
	d1 = roll_a_die()
	d2 = roll_a_die()
	return d1, d1 + d2
# 在已知道 x 的条件下求 y 的分布是很容易的
def random_y_given_x(x):
	"""equally likely to be x + 1, x + 2, ... , x + 6"""
	return x + roll_a_die()
# 如果将已知条件反过来，事情会变得更加复杂。
def random_x_given_y(y):
	if y <= 7:
		# 如果点数为7或以下的数，那么第一个骰子的点数有等同的机会为
		# 1, 2, …, (总点数 - 1)
		return random.randrange(1, y)
	else:
		# 如果点数为7或以上的数，那么第一个骰子的点数有等同的机会为
		# (total - 6), (总点数 - 5), …, 6
		return random.randrange(y - 6, 7)

# 重复一定次数后，得到的x 值和 y 值就可以作为根据无条件的联合分布获取的样本了：
def gibbs_sample(num_iters=100):
	x, y = 1, 2 # doesn't really matter
	for _ in range(num_iters):
		x = random_x_given_y(y)
		y = random_y_given_x(x)
	return x, y
# 通过下列代码你会发现，这种取样方法与直接取样的效果相似：
def compare_distributions(num_samples=1000):
	counts = defaultdict(lambda: [0, 0])
	for _ in range(num_samples):
		counts[gibbs_sample()][0] += 1
		counts[direct_sample()][1] += 1
	return counts
print(compare_distributions())