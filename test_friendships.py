# coding: utf-8

# 数据是一个包含所有用户的列表。
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

# 同时，他也给了你用户的“友邻关系”数据列表。
friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
 (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

# 如果我们希望对每个用户增加一个朋友列表，
# 首先需要对每个用户创建一个空列表：
for user in users:
	user["friends"] = []
# 再用 friendships 数据填充
for i, j in friendships: 
	 # 这能起作用是因为users[i]是id为i的用户
	 users[i]["friends"].append(users[j]) # 把i加为j的朋友
	 users[j]["friends"].append(users[i]) # 把j加为i的朋友
# print("users : \n", users)

# 首先计算出全部的联系数，这需要对所有用户的 friends 列表的长度求和：
def number_of_friends(user):
	"""how many friends does _user_have?"""
	return len(user["friends"]) # 列表friend_ids的长度
total_connections = sum(number_of_friends(user)
 	for user in users) # 24
print("total_connections : ", total_connections)

# 然后，将它除以用户个数：
# from __future__ import division # 整数除法需要导入
num_users = len(users) # 列表users的长度
print("num_users : ", num_users)
avg_connections = total_connections / num_users # 2.4
print("avg_connections : ", avg_connections)

# 因为用户不多，所以能很方便地按照朋友数的多少排序：
# 创建一个列表(user_id, number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user))
					for user in users]
# 把它按照num_friends从最大到最小排序
# sorted(num_friends_by_id,                       
# 		 key=lambda (user_id, num_friends): num_friends, 
#		 reverse=True)
sorted(num_friends_by_id, key=lambda x: x[1], reverse=True)
print("num_friends_by_id : ", num_friends_by_id)

# 为了排除那些已经成为朋友的用户，我们需要设计一个辅助函数来实现这个功能：
from collections import Counter # 默认未加载
# 一个计数器将一个序列的值转化成一个类似于整型的标准字典（即 defaultdict(int)）的
# 键到计数的对象映射。我们主要用它来生成直方图，例如：
# c = Counter([0, 1, 2, 0]) # c是（基本的） { 0 : 2, 1 : 1, 2 : 1 }
def not_the_same(user, other_user):  # 不是我
	"""two users are not the same if they have different ids"""
	return user["id"] != other_user["id"]
def not_friends(user, other_user):   # 不是我的朋友
	"""other_user is not a friend if he's not in user["friends"];
	   that is, if he's not_the_same as all the people in user["friends"]"""
	return all(not_the_same(friend, other_user)
	 			for friend in user["friends"])
def friends_of_friend_ids(user):
	# 这里使用了列表解析技巧。包含多个for语句和if条件。
	return Counter(foaf["id"]
		for friend in user["friends"]           # 对我的每一位朋友
			for foaf in friend["friends"]       # 计数他们的朋友
				if not_the_same(user, foaf)     # 既不是我
				   and not_friends(user, foaf)) # 也不是我的朋友
# Counter({0: 2, 5: 1})
print("friends_of_friend_ids : ", friends_of_friend_ids(users[3])) 

# 下面是有共同兴趣的人的列表。
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

# 找出对某种事物有共同爱好的用户，很容易设计出相应的函数：
def data_scientists_who_like(target_interest):
    return [user_id 
            for user_id, user_interest in interests 
            if user_interest == target_interest]

# 建立一个从兴趣到用户的索引直接搜索：
from collections import defaultdict
# 键是interest，值是带有这个interest的user_id的列表
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
	user_ids_by_interest[interest].append(user_id)
# 以及另一个从用户到兴趣的索引：
# 键是user_id，值是对那些user_id的interest的列表
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
	interests_by_user_id[user_id].append(interest)

# 给定一个用户，可以方便地找到与他共同爱好最多的用户：
#   • 迭代这个用户的兴趣；
#   • 针对这个用户的每一种兴趣，寻找这种兴趣的其他用户，并迭代；
#   • 记录每一个用户在循环中出现的次数。
def most_common_interests_with(user):
	return Counter(interested_user_id
		for interest in interests_by_user_id[user["id"]]
		for interested_user_id in user_ids_by_interest[interest]
		if interested_user_id != user["id"])

