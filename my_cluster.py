# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *

import math
import random
from collections import defaultdict

def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))

# 利用 vector_mean 函数，可以轻松创建如下所示的类来完成上述工作：
class KMeans:
	"""performs k-means clustering"""
	def __init__(self, k):
		self.k = k # 聚类的数目
		self.means = None # 聚类的均值
	def classify(self, input):
		"""return the index of the cluster closest to the input"""
		return min(range(self.k),
				key=lambda i: squared_distance(input, self.means[i]))
	def train(self, inputs):
		# 选择k个随机点作为初始的均值
		self.means = random.sample(inputs, self.k)
		assignments = None
		while True:
			# 查找新分配
			# new_assignments = map(self.classify, inputs)
			# 为什么使用list会变快？？？
			new_assignments = list(map(self.classify, inputs))
			# 如果所有数据点都不再被重新分配，那么就停止
			if assignments == new_assignments:
				return
			# 否则就重新分配
			assignments = new_assignments
			# print("assignments : ", assignments)
			# 并基于新的分配计算新的均值
			for i in range(self.k):
				# 查找分配给聚类i的所有的点
				i_points = [p for p, a in 
					zip(inputs, assignments) if a == i]
				# 确保i_points不是空的，因此除数不会是0
				if i_points:
					self.means[i] = vector_mean(i_points)

# 以误差（即每个数据点到所在聚类的中心的距离）的平方之和作为 k 的函数，
# 画出该函数的图像，并在其“弯曲”的地方寻找合适的取值：
def squared_clustering_errors(inputs, k):
	"""finds the total squared error from k-means clustering the inputs"""
	clusterer = KMeans(k)
	clusterer.train(inputs)
	means = clusterer.means
	assignments = map(clusterer.classify, inputs)
	return sum(squared_distance(input, means[cluster])
			for input, cluster in zip(inputs, assignments))

# 先来创建一些辅助函数：
def is_leaf(cluster):
	"""a cluster is a leaf if it has length 1"""
	return len(cluster) == 1
def get_children(cluster):
	"""returns the two children of this cluster if it's a merged cluster;
	raises an exception if this is a leaf cluster"""
	if is_leaf(cluster):
		raise TypeError("a leaf cluster has no children")
	else:
		return cluster[1]
def get_values(cluster):
	"""returns the value in this cluster (if it's a leaf cluster)
	or all the values in the leaf clusters below it (if it's not)"""
	if is_leaf(cluster):
		return cluster # 已经是一个包含值的一元组
	else:
		return [value
			for child in get_children(cluster)
			for value in get_values(child)]

# 使用两个聚类的元素之间的最小距离，据此将两个挨得最近的聚类合并。
def cluster_distance(cluster1, cluster2, distance_agg=min):
	"""compute all the pairwise distances between cluster1 and cluster2
	and apply _distance_agg_ to the resulting list"""
	return distance_agg([distance(input1, input2)
				for input1 in get_values(cluster1)
				for input2 in get_values(cluster2)])
# 借助合并次序踪迹（slot）来跟踪合并的顺序
def get_merge_order(cluster):
	if is_leaf(cluster):
		return float('inf')
	else:
		return cluster[0] # merge_order是二元组中的第一个元素
# 现在我们可以创建聚类算法了：
def bottom_up_cluster(inputs, distance_agg=min):
	# 最开始每个输入都是一个叶聚类/一元组
	clusters = [(input,) for input in inputs]
	# 只要剩余一个以上的聚类……
	while len(clusters) > 1:
		# 就找出最近的两个聚类
		c1, c2 = min([(cluster1, cluster2)
			for i, cluster1 in enumerate(clusters)
			for cluster2 in clusters[:i]],
			# key=lambda (x, y): cluster_distance(x, y, distance_agg))
			key=lambda p: cluster_distance(p[0], p[1], distance_agg))
		# 从聚类列表中将它们移除
		clusters = [c for c in clusters if c != c1 and c != c2]
		# 使用merge_order = 剩余聚类的数目来合并它们
		merged_cluster = (len(clusters), [c1, c2])
		# 并添加它们的合并
		clusters.append(merged_cluster)
	# 当只剩一个聚类时，返回它
	return clusters[0]

# 下面让我们来写一个函数，
# 使其可以通过执行适当次数的分拆动作来产生任意数量的聚类：
def generate_clusters(base_cluster, num_clusters):
	# 开始的列表只有基本聚类
	clusters = [base_cluster]
	# 只要我们还没有足够的聚类……
	while len(clusters) < num_clusters:
		# 选择上一个合并的聚类
		next_cluster = min(clusters, key=get_merge_order)
		# 将它从列表中移除
		clusters = [c for c in clusters if c != next_cluster]
		# 并将它的子聚累添加到列表中（即拆分它）
		clusters.extend(get_children(next_cluster))
	# 一旦我们有了足够的聚类……
	return clusters





