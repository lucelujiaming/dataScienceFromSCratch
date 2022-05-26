# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *

import math
import random
from collections import defaultdict

# 我们用熵（entropy）这个概念来指代“信息含量”，
# 我们可以轻而易举地将上面的定义编写为一个函数：
def entropy(class_probabilities):
	"""given a list of class probabilities, compute the entropy"""
	return sum(-p * math.log(p, 2)
			for p in class_probabilities
			if p) # 忽略零可能性

# 类别概率需要我们自己来计算。
def class_probabilities(labels):
	total_count = len(labels)
	return [count / total_count
		for count in Counter(labels).values()]
def data_entropy(labeled_data):
	labels = [label for _, label in labeled_data]
	probabilities = class_probabilities(labels)
	return entropy(probabilities)

# 我们就可以通过如下加权和的形式来计算这次划分的熵：
# 下面是具体的实现代码：
def partition_entropy(subsets):
	"""find the entropy from this partition of data into subsets
	subsets is a list of lists of labeled data"""
	total_count = sum(len(subset) for subset in subsets)
	return sum( data_entropy(subset) * len(subset) / total_count
			for subset in subsets )

# 副总为你提供了应聘者的相关资料
inputs = [
 ({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'no'}, False),
 ({'level':'Senior', 'lang':'Java', 'tweets':'no', 'phd':'yes'}, False),
 ({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
 ({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, True),
 ({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
 ({'level':'Junior', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, False),
 ({'level':'Mid', 'lang':'R', 'tweets':'yes', 'phd':'yes'}, True),
 ({'level':'Senior', 'lang':'Python', 'tweets':'no', 'phd':'no'}, False),
 ({'level':'Senior', 'lang':'R', 'tweets':'yes', 'phd':'no'}, True),
 ({'level':'Junior', 'lang':'Python', 'tweets':'yes', 'phd':'no'}, True),
 ({'level':'Senior', 'lang':'Python', 'tweets':'yes', 'phd':'yes'}, True),
 ({'level':'Mid', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, True),
 ({'level':'Mid', 'lang':'Java', 'tweets':'yes', 'phd':'no'}, True),
 ({'level':'Junior', 'lang':'Python', 'tweets':'no', 'phd':'yes'}, False)
]

# 我们首先要做的就是找出熵最小的分割方法。我们将通过如下函数来完成分割：
def partition_by(inputs, attribute):
	"""each input is a pair (attribute_dict, label).
	returns a dict : attribute_value -> inputs"""
	groups = defaultdict(list)
	for input in inputs:
		key = input[0][attribute] # 得到特定属性的值
		groups[key].append(input) # 然后把这个输入加到正确的列表中
	return groups
# 我们可以通过下列代码来计算熵：
def partition_entropy_by(inputs, attribute):
	"""computes the entropy corresponding to the given partition"""
	partitions = partition_by(inputs, attribute)
	return partition_entropy(partitions.values())
# 然后我们只需要找出在整个数据集上具有最小熵的分割即可：
for key in ['level','lang','tweets','phd']:
	print("for key in ['level','lang','tweets','phd'] ", key, " : ",
		key, partition_entropy_by(inputs, key))

senior_inputs = [(input, label)
	for input, label in inputs if input["level"] == "Senior"]
for key in ['lang', 'tweets', 'phd']:
	print("['lang', 'tweets', 'phd'] ", key, " : ",
		key, partition_entropy_by(senior_inputs, key))

# 给定了表示方法后，我们就可以对输入进行分类了，具体如下所示：
def classify(tree, input):
	"""classify the input using the given decision tree"""
	# 如果这是一个叶节点，则返回其值
	if tree in [True, False]:
		return tree
	# 否则这个树就包含一个需要划分的属性
	# 和一个字典，字典的键是那个属性的值
	# 值是下一步需要考虑的子树
	attribute, subtree_dict = tree
	subtree_key = input.get(attribute) # 如果输入的是缺失的属性，则返回None
	if subtree_key not in subtree_dict: # 如果键没有子树
		subtree_key = None # 则需要用到None子树
	subtree = subtree_dict[subtree_key] # 选择恰当的子树
	return classify(subtree, input) # 并用它来对输入分类
# 最后要做的就是利用训练数据建立决策树的具体表示形式：
def build_tree_id3(inputs, split_candidates=None):
	# 如果这是第一步
	# 第一次输入的所有的键就都是split candidates
	if split_candidates is None:
		split_candidates = inputs[0][0].keys()
	# 对输入里的True和False计数
	num_inputs = len(inputs)
	num_trues = len([label for item, label in inputs if label])
	num_falses = num_inputs - num_trues

	if num_trues == 0: return False # 若没有True，则返回一个"False"叶节点
	if num_falses == 0: return True # 若没有False，则返回一个"True"叶节点

	if not split_candidates: # 若不再有split candidates
		return num_trues >= num_falses # 则返回多数叶节点
	# 否则在最好的属性上进行划分
	best_attribute = min(split_candidates,
			key=partial(partition_entropy_by, inputs))
	partitions = partition_by(inputs, best_attribute)
	new_candidates = [a for a in split_candidates
	if a != best_attribute]
	# 递归地创建子树
	subtrees = { attribute_value : build_tree_id3(subset, new_candidates)
			 for attribute_value, subset in partitions.items() }
	subtrees[None] = num_trues > num_falses # 默认情况
	return (best_attribute, subtrees)

tree = build_tree_id3(inputs)
retClassOne = classify(tree, { "level" : "Junior",
				"lang" : "Java",
				"tweets" : "yes",
				"phd" : "no"} ) # True
print(retClassOne)
retClassTwo = classify(tree, { "level" : "Junior",
				"lang" : "Java",
				"tweets" : "yes",
				"phd" : "yes"} ) # False
print(retClassTwo)

retClassThird = classify(tree, { "level" : "Intern" } ) # True
print(retClassThird)
retClassFour  = classify(tree, { "level" : "Senior" } ) # False
print(retClassFour)

# 使用随机森林（random forest）技术。
# 我们可以建立多个决策树，然后通过投票方式决定如何对输入进行分类：
def forest_classify(trees, input):
	votes = [classify(tree, input) for tree in trees]
	vote_counts = Counter(votes)
	return vote_counts.most_common(1)[0][0]

#	# 从中随机选取一个子集，然后从中寻找最佳属性进行划分：
#	# 如果已经存在了几个足够的划分候选项，就查看全部
#	if len(split_candidates) <= self.num_split_candidates:
#		sampled_split_candidates = split_candidates
#	# 否则选取一个随机样本
#	else:
#		sampled_split_candidates = random.sample(split_candidates,
#	 			self.num_split_candidates)
#	# 现在仅从这些候选项中选择最佳属性
#	best_attribute = min(sampled_split_candidates,
#					key=partial(partition_entropy_by, inputs))
#	partitions = partition_by(inputs, best_attribute)








