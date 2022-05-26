# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *
from my_cluster import *

import math
import random
from collections import defaultdict

inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],
		[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],
		[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

random.seed(0) # 因此你得到的结果与我的一样
clusterer = KMeans(3)
clusterer.train(inputs)
print(clusterer.means)

# 现在画出1至len（输入）的聚类图
ks = range(1, len(inputs) + 1)
errors = [squared_clustering_errors(inputs, k) for k in ks]
plt.plot(ks, errors)
plt.xticks(ks)
plt.xlabel("k")
plt.ylabel("误差的平方之和")
plt.title("总误差与聚类数目")
plt.show()


base_cluster = bottom_up_cluster(inputs)
print(base_cluster)

# 举例来说，如果我们想要生成三个聚类，可以使用下列代码：
three_clusters = [get_values(cluster)
		for cluster in generate_clusters(base_cluster, 3)]
# 利用下面的代码，我们可以轻松绘制其图形：
for i, cluster, marker, color in zip([1, 2, 3],
								three_clusters,
								['D','o','*'],
								['r','g','b']):
	xs, ys = zip(*cluster) # 魔法般的解压方式
	plt.scatter(xs, ys, color=color, marker=marker)
	# 向聚类的均值添加一个数字
	x, y = vector_mean(cluster)
	plt.plot(x, y, marker='$' + str(i) + '$', color='black')

plt.title("利用最短距离得到的三个自下而上的聚类")
plt.xlabel("市中心以东的街区")
plt.ylabel("市中心以北的街区")
plt.show()
