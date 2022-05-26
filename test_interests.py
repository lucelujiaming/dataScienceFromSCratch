# coding: utf-8

from collections import Counter # 默认未加载
# 来自友邻推荐项目的原始数据：
interests = [
	(0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
	(0, "Spark"), (0, "Storm"), (0, "Cassandra"),
	(1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
	(1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
	(2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
	(3, "statistics"), (3, "regression"), (3, "probability"),
	(4, "machine learning"), (4, "regression"), (4, "decision trees"),
	(4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
	(5, "Haskell"), (5, "programming languages"), (6, "statistics"),
	(6, "probability"), (6, "mathematics"), (6, "theory"),
	(7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
	(7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
	(8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
	(9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

# 用下面的代码，数一下兴趣词汇的个数：
#   1. 小写每一种兴趣（因为不同的用户不一定会大写他们的兴趣）；
#   2. 把它划分为单词；
#   3. 数一数结果。
words_and_counts = Counter(word
	for user, interest in interests
	for word in interest.lower().split())

# 列出出现一次以上的词汇是很容易的：
for word, count in words_and_counts.most_common():
	if count > 1:
		print("word, count : ", word, count)