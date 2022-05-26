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

# 这里要考察的 users_interests 是之前就曾用过的一个数据集：
users_interests = [
	["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
	["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
	["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
	["R", "Python", "statistics", "regression", "probability"],
	["machine learning", "regression", "decision trees", "libsvm"],
	["Python", "R", "Java", "C++", "Haskell", "programming languages"],
	["statistics", "probability", "mathematics", "theory"],
	["machine learning", "scikit-learn", "Mahout", "neural networks"],
	["neural networks", "deep learning", "Big Data", "artificial intelligence"],
	["Hadoop", "Java", "MapReduce", "Big Data"],
	["statistics", "R", "statsmodels"],
	["C++", "deep learning", "artificial intelligence", "probability"],
	["pandas", "R", "Python"],
	["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
	["libsvm", "regression", "support vector machines"]
]
# 同时，我们要考虑如何根据用户当前特定的兴趣来向其推荐新的感兴趣的东西。
# 一个比较简单的方法就是直接推荐比较流行的东西：
popular_interests = Counter(interest
	for user_interests in users_interests
	for interest in user_interests).most_common()

# 完成上述计算后，我们就可以向用户推荐那些当前最流行的、他尚未感兴趣的东西：
def most_popular_new_interests(user_interests, max_results=5):
	suggestions = [(interest, frequency)
				for interest, frequency in popular_interests
				if interest not in user_interests]
	return suggestions[:max_results]

# 我们需要找到一种指标来衡量两个用户之间的相似程度。这里使用余弦相似度
def cosine_similarity(v, w):
	if dot(v, v) != 0:
		if dot(w, w) != 0:
			return dot(v, w) / math.sqrt(dot(v, v) * dot(w, w))
		else:
			return 0
	else:
		return 0

# 在这个列表中的第一个兴趣就是兴趣 0，其他以此类推：
unique_interests = sorted(list({ interest
				for user_interests in users_interests
				for interest in user_interests }))

# 接下来，我们要给每个用户生成一个由 0 和 1 组成的“兴趣”向量。
def make_user_interest_vector(user_interests):
	"""given a list of interests, produce a vector whose ith element is 1
	if unique_interests[i] is in the list, 0 otherwise"""
	return [1 if interest in user_interests else 0
			 for interest in unique_interests]

# 我们还可以创建用户兴趣矩阵，
# 为此，我们只需将这个函数映射到由用户的兴趣构成的列表的列表上面即可：
user_interest_matrix = list(map(make_user_interest_vector, users_interests))

# 由于我们的数据集非常小，因此所有用户两两之间的相似性的计算量不是很大：
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
						for interest_vector_j in user_interest_matrix]
						for interest_vector_i in user_interest_matrix]

# 面我们按照相似度从大到小的顺序对结果进行排序：
def most_similar_users_to(user_id):
	pairs = [(other_user_id, similarity) # 查找
		for other_user_id, similarity in # 其他用户
			enumerate(user_similarities[user_id]) # 非零
		if user_id != other_user_id and similarity > 0] # 相似度
	return sorted(pairs, # 将其排序
			key=lambda similarity: similarity, # 相似度
			reverse=True) # 由大到小
print("most_similar_users_to(0) : ", most_similar_users_to(0))

# 对于每种兴趣，我们可以将其他对其感兴趣的用户的用户相似度加起来：
def user_based_suggestions(user_id, include_current_interests=False):
	# 将相似度加起来
	suggestions = defaultdict(float)
	for other_user_id, similarity in most_similar_users_to(user_id):
		for interest in users_interests[other_user_id]:
			suggestions[interest] += similarity
	# 将它们转化成已排序的列表
	suggestions = sorted(suggestions.items(),
						key=lambda weight: weight,
						reverse=True)
	# 并且（有可能）排除已存在的兴趣
	if include_current_interests:
		return suggestions
	else:
		return [(suggestion, weight)
			 for suggestion, weight in suggestions
			  if suggestion not in users_interests[user_id]]

# 对用户兴趣矩阵进行转置（transpose），以使行对应于兴趣，列对应于用户：
interest_user_matrix = [[user_interest_vector[j]
			for user_interest_vector in user_interest_matrix]
			for j, _ in enumerate(unique_interests)]
print("interest_user_matrix : ", interest_user_matrix)

# 现在，我们可以再次利用余弦相似度。如果喜欢两个主题的用户完全重合，那么它们的相似度为 1。
# 如果喜欢两个主题的用户没有一个是重合的，那么它们的相似度将是 0：
interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
					for user_vector_j in interest_user_matrix]
					for user_vector_i in interest_user_matrix]

# 我们可以通过下列代码找出与 Big Data（兴趣 0）最相似的项：
def most_similar_interests_to(interest_id):
	similarities = interest_similarities[interest_id]
	pairs = [(unique_interests[other_interest_id], similarity)
		for other_interest_id, similarity in enumerate(similarities)
		if interest_id != other_interest_id and similarity > 0]
	return sorted(pairs,
			# key=lambda similarity: similarity,
			key=lambda pair: pair[1],
			reverse=True)
print("most_similar_interests_to(0) : ", most_similar_interests_to(0))

 # 我们可以通过总结与其兴趣相似的东西来为其提供建议：
def item_based_suggestions(user_id, include_current_interests=False):
	# 将相似的兴趣相加
	suggestions = defaultdict(float)
	user_interest_vector = user_interest_matrix[user_id]
	for interest_id, is_interested in enumerate(user_interest_vector):
		if is_interested == 1:
			similar_interests = most_similar_interests_to(interest_id)
			for interest, similarity in similar_interests:
				suggestions[interest] += similarity
	# 根据权重将其排序
	suggestions = sorted(suggestions.items(),
				# key=lambda similarity: similarity,
				key=lambda pair: pair[1],
				reverse=True)
	if include_current_interests:
		return suggestions
	else:
		return [(suggestion, weight)
			for suggestion, weight in suggestions
			if suggestion not in users_interests[user_id]]
print("item_based_suggestions(0) : ", item_based_suggestions(0))







