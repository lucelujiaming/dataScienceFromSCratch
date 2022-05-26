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

# 首先，我们需要一个函数，根据任意一组权重来随机选择一个索引：
def sample_from(weights):
	"""returns i with probability weights[i] / sum(weights)"""
	total = sum(weights)
	rnd = total * random.random() # 在0和总数之间均匀分布
	for i, w in enumerate(weights):
		rnd -= w # 返回最小的i
		if rnd <= 0: return i # 因此weights[0] + … + weights[i] >= rnd

# 我们的文档包含的是用户的各种兴趣，看起来可能像下面这样：
documents = [
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

K = 4
# 我们要统计每个文档中每个主题出现的次数，代码如下：
# 计数的一个列表，每个文档各有一个列表
document_topic_counts = [Counter() for _ in documents]
# 我们要统计每个主题中每个单词出现的次数，代码如下：
# 计数的一个列表，每个主题各有一个列表
topic_word_counts = [Counter() for _ in range(K)]
# 我们要知道每个主题中单词的总数，代码如下：
# 数字的一个列表, 每个主题各有一个列表
topic_counts = [0 for _ in range(K)]
# 下面的代码统计每个文档中的单词总数：
# 数字的一个列表，每个文档各有一个列表
# document_lengths = map(len, documents)
document_lengths = [len(d) for d in documents]

# 下面代码统计不同单词的数量：
distinct_words = set(word for document in documents for word in document)
W = len(distinct_words)
# 另外，下列代码可以用来统计文档的数量：
D = len(documents)
# 一旦掌握了这些数据，我们就可以了解（比如说）documents[3] 中
# 与主题 1 相关的单词的数量，如下所示：
document_topic_counts[3][1]
# 同时，我们还可以找出与主题 2 相关的单词 nlp 出现的次数，具体代码如下所示：
topic_word_counts[2]["nlp"]

# 现在，我们已经为定义条件概率函数做好了准备。
def p_topic_given_document(topic, d, alpha=0.1):
    """the fraction of words in document _d_
    that are assigned to _topic_ (plus some smoothing)"""
    return ((document_topic_counts[d][topic] + alpha) /
            (document_lengths[d] + K * alpha))
def p_word_given_topic(word, topic, beta=0.1):
    """the fraction of words assigned to _topic_
    that equal _word_ (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) /
            (topic_counts[topic] + W * beta))
# 然后利用下列代码给更新中的主题确定权重：
def topic_weight(d, word, k):
    """given a document and a word in that document,
    return the weight for the kth topic"""
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)
def choose_new_topic(d, word):
    return sample_from([topic_weight(d, word, k)
                    for k in range(K)])

# 这就是我们所需要的全部零部件。
# 下面，我们开始将每个单词随机指派给一个话题，并计入相应的计数器：
random.seed(0)
document_topics = [[random.randrange(K) for word in document]
for document in documents]
for d in range(D):
    for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1
print("document_topics : ", document_topics)

 # 我们的目标是利用主题 - 单词分布和文档 - 主题分布进行联合采样。
 # 为此，我们可以通过之前定义的条件概率进行吉布斯采样，具体代码如下所示：
for iter in range(1000):
    for d in range(D):
        for i, (word, topic) in enumerate(zip(documents[d],
            document_topics[d])):
            # 从计数中移除这个单词/主题
            # 以便它不会影响权重
            document_topic_counts[d][topic] -= 1
            topic_word_counts[topic][word] -= 1
            topic_counts[topic] -= 1
            document_lengths[d] -= 1

            # 基于权重选择一个新的主题
            new_topic = choose_new_topic(d, word)
            document_topics[d][i] = new_topic

            # 现在把它重新加到计数中
            document_topic_counts[d][new_topic] += 1
            topic_word_counts[new_topic][word] += 1
            topic_counts[new_topic] += 1
            document_lengths[d] += 1


 # 下面，让我们来找出权重较大的 5 个单词，具体代码如下所示：
for k, word_counts in enumerate(topic_word_counts):
    for word, count in word_counts.most_common():
        if count > 0: 
            print(k, word, count)

# 根据这些数据，我们就可以给主题取名了：
topic_names = ["Big Data and programming languages",
                "Python and statistics",
                "databases",
                "machine learning"]
# 至此我们就清楚模型是如何将主题分配到每个用户的兴趣上面了：
for document, topic_counts in zip(documents, document_topic_counts):
    print("document : ", document)
    for topic, count in topic_counts.most_common():
        if count > 0:
            print(topic_names[topic], count)
