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


users = [
	 { "id": 0, "name": "Hero" },
	 { "id": 1, "name": "Dunn" },
	 { "id": 2, "name": "Sue" },
	 { "id": 3, "name": "Chi" },
	 { "id": 4, "name": "Thor" },
	 { "id": 5, "name": "Clive" },
	 { "id": 6, "name": "Hicks" },
	 { "id": 7, "name": "Devin" },
	 { "id": 8, "name": "Kate" },
	 { "id": 9, "name": "Klein" }
]
# 以及用户之间的好友关系：
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
 (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# 给每个用户的 dict 结构添加了相应的朋友列表：
for user in users:
	user["friends"] = []
for i, j in friendships:
	# 这能奏效是因为users[i]是id为i的用户
	users[i]["friends"].append(users[j]) # 添加i作为j的朋友
	users[j]["friends"].append(users[i]) # 添加j作为i的朋友

# 作为第一步，我们需要找出所有用户对之间的最短路径。
# 将采用效率虽低一些但更加容易理解的一个广度优先搜索的算法。
# 我们可以将这些步骤放入一个（大型）函数中，代码如下所示：
from collections import deque
def shortest_paths_from(from_user):
	# 一个由"user_id"到该用户所有最短路径的字典
	shortest_paths_to = { from_user["id"] : [[]] }
	# 我们需要检查的(previous user, next user)队列
	# 从所有(from_user, friend_of_from_user)对开始着手
	frontier = deque((from_user, friend)
			for friend in from_user["friends"])
	# 直到队列为空为止
	while frontier:
		prev_user, user = frontier.popleft() # 删除该用户
		user_id = user["id"] # 即队列中的第一个用户
		# 若要向队列添加内容
		# 我们必须知道通向prev_user的某些最短路径
		paths_to_prev_user = shortest_paths_to[prev_user["id"]]
		new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]
		# 我们可能已经知道了一条最短路径
		old_paths_to_user = shortest_paths_to.get(user_id, [])
		# 到目前为止，我们看到的到达这里的最短路径有多长？
		if old_paths_to_user:
			min_path_length = len(old_paths_to_user[0])
		else:
			min_path_length = float('inf')
		# 只留下那些刚找到的不太长的路径
		new_paths_to_user = [path
		for path in new_paths_to_user
		if len(path) <= min_path_length
		and path not in old_paths_to_user]
	shortest_paths_to[user_id] = old_paths_to_user + new_paths_to_user
	# 将这些从未谋面的"邻居"添加到frontier中
	frontier.extend((user, friend)
			for friend in user["friends"]
			if friend["id"] not in shortest_paths_to)
	return shortest_paths_to
# 现在我们可以将这些 dict 存放到各个节点中了：
for user in users:
 user["shortest_paths"] = shortest_paths_from(user)

# 好了，现在终于可以计算中介中心度了。
for user in users:
	user["betweenness_centrality"] = 0.0
for source in users:
	source_id = source["id"]
	for target_id, paths in source["shortest_paths"].items():
		if source_id < target_id: # 不要加倍计数
			num_paths = len(paths) # 有多少最短路径
			contrib = 1 / num_paths # 中心度加1/n
			for path in paths:
				for id in path:
					if id not in [source_id, target_id]:
						users[id]["betweenness_centrality"] += contrib

# 由于我们已经计算出每一对节点之间的最短路径，因此，只要对其求和即可。
def farness(user):
	"""the sum of the lengths of the shortest paths to each other user"""
	return sum(len(paths[0])
				for paths in user["shortest_paths"].values())
# 这样一来，接近中心度的计算量就很小了
for user in users:
	user["closeness_centrality"] = 1 / farness(user)

# 下面实现矩阵乘法
# 计算矩阵 A 的第 i 行与矩阵 B 的第 j 列的点积，具体代码如下所示：
def matrix_product_entry(A, B, i, j):
	return dot(get_row(A, i), get_column(B, j))

# 以通过下列代码实现矩阵的乘法运算了：
def matrix_multiply(A, B):
	n1, k1 = shape(A)
	n2, k2 = shape(B)
	if k1 != n2:
		raise ArithmeticError("incompatible shapes!")
	return make_matrix(n1, k2, partial(matrix_product_entry, A, B))

# 要定义相应的辅助函数，以便实现向量和列表两种表示形式之间的转换：
def vector_as_matrix(v):
	"""returns the vector v (represented as a list) as a n x 1 matrix"""
	return [[v_i] for v_i in v]
def vector_from_matrix(v_as_matrix):
	"""returns the n x 1 matrix as a list of values"""
	return [row[0] for row in v_as_matrix]

# 如此一来，我们就可以利用 matrix_multiply 来定义矩阵运算了：
def matrix_operate(A, v):
	v_as_matrix = vector_as_matrix(v)
	product = matrix_multiply(A, v_as_matrix)
	return vector_from_matrix(product)

# 确定矩阵 A 的特征向量的一种可行方法是取一个随机向量 v，
# 然后利用 matrix_operate 对其进行调整，
# 从而得到一个长度为 1 的向量，重复该过程直到收敛为止：
def find_eigenvector(A, tolerance=0.00001):
	guess = [random.random() for __ in A]
	while True:
		result = matrix_operate(A, guess)
		length = magnitude(result)
		next_guess = scalar_multiply(1/length, result)
		if distance(guess, next_guess) < tolerance:
			return next_guess, length # eigenvector, eigenvalue
			guess = next_guess

# 需要用 adjacency_matrix 来表示网络中的连接
def entry_fn(i, j):
	return 1 if (i, j) in friendships or (j, i) in friendships else 0
n = len(users)
adjacency_matrix = make_matrix(n, n, entry_fn)

# 我们只要借助于 find_eigenvector 函数就能够找到这种 adjacency_matrix。
eigenvector_centralities, _ = find_eigenvector(adjacency_matrix)

# 下面加入赞助列表。
endorsements = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2),
 (2, 1), (1, 3), (2, 3), (3, 4), (5, 4),
 (5, 6), (7, 5), (6, 8), (8, 7), (8, 9)]
for user in users:
	user["endorses"] = [] # 增加一个列表来追踪外方的赞助
	user["endorsed_by"] = [] # 增加另外一个列表来追踪赞助
for source_id, target_id in endorsements:
	users[source_id]["endorses"].append(users[target_id])
	users[target_id]["endorsed_by"].append(users[source_id])

# 找出 most_endorsed（最受推崇的）数据科学家，从而将这些信息出售给猎头们：
endorsements_by_id = [(user["id"], len(user["endorsed_by"]))
						for user in users]
sorted(endorsements_by_id,
		key=lambda  num_endorsements : num_endorsements,
		reverse=True)

# 来自得票数较多的人的投票的分量应该重于得票数较少的那些人的投票。
# 这实际上就是 PageRank 算法的思想精华，Google 就是利用它来给网站排名的。
# 下面是这种思想的简化版本。
# 1. 网络中 PageRank 的总分数为 1（或 100%）。
# 2. 最初，这个 PageRank 被均匀分布到网络的各个节点中。
# 3. 在每一步中，每个节点的 PageRank 很大一部分将均匀分布到其外部链接中。
# 4. 在每个步骤中，每个节点的 PageRank 的其余部分被均匀地分布到所有节点上。
def page_rank(users, damping = 0.85, num_iters = 100):
	# 一开始均匀分布PageRank
	num_users = len(users)
	pr = { user["id"] : 1 / num_users for user in users }
	# 这是PageRank的一小部分
	# 每个节点进行各自的迭代
	base_pr = (1 - damping) / num_users
	for __ in range(num_iters):
		next_pr = { user["id"] : base_pr for user in users }
		for user in users:
			# 将PageRank分布到外部链接中
			links_pr = pr[user["id"]] * damping
			for endorsee in user["endorses"]:
				next_pr[endorsee["id"]] += links_pr / len(user["endorses"])
		pr = next_pr
	return pr

print("page_rank : ", page_rank(users))

