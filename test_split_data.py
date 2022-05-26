# coding: utf-8

import random
# 划分数据集
def split_data(data, prob):
	"""split data into fractions [prob, 1 - prob]"""
	results = [], []
	for row in data:
		results[0 if random.random() < prob else 1].append(row)
	return results
# 通常我们会有一个作为输入变量的矩阵 x 和一个作为输出变量的向量 y。
# 这种情况下，我们要确保无论在训练数据还是测试数据中，都要把对应的值放在一起：
def train_test_split(x, y, test_pct):
	data = zip(x, y) # 成对的对应值
	train, test = split_data(data, 1 - test_pct) # 划分这个成对的数据集
	# Python 内置函数zip() 函数用于将可迭代的对象作为参数,
	# 将对象中对应的元素打包成一个个元组,然后返回由这些元组组成的列表。

	x_train, y_train = zip(*train) # 魔法般的解压技巧
	x_test, y_test = zip(*test)
	return x_train, x_test, y_train, y_test
