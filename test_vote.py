# coding: utf-8

# 我们需要一个函数来计算投票结果。一个可能的函数是：
from collections import Counter # 默认未加载
def raw_majority_vote(labels):
    votes = Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner

# 减少 k 值直到找到唯一的获胜者。
def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
            for count in vote_counts.values()
            if count == winner_count])
    if num_winners == 1:
        return winner # 唯一的获胜者，返回它的值
    else:
        return majority_vote(labels[:-1]) # 去掉最远元素，再次尝试

from my_linear_algebra import *
def sort_function(point, new_point):
    return distance(point, new_point)
# 使用这个函数很容易创建一个分类器：
def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""
    # 把标记好的点按从最近到最远的顺序排序
    by_distance = sorted(list(labeled_points),
            key=lambda point : 
                distance(list(point), list(new_point)))
    #        key=sort_function())
    # 寻找k个最近邻的标签
    k_nearest_labels = [label for _, label in by_distance[:k]]
    # 然后让它们投票
    return majority_vote(k_nearest_labels)

