# coding: utf-8

import math
import random, re
from collections import defaultdict

class Table:
 def __init__(self, columns):
 self.columns = columns
 self.rows = []
def __repr__(self):
"""pretty representation of the table: columns then rows"""
return str(self.columns) + "\n" + "\n".join(map(str, self.rows))
 def insert(self, row_values):
if len(row_values) != len(self.columns):
raise TypeError("wrong number of elements")
 row_dict = dict(zip(self.columns, row_values))
 self.rows.append(row_dict)
 # 我们将为 NotQuiteABase 增加类似的 update 方法。
 def update(self, updates, predicate):
for row in self.rows:
if predicate(row):
for column, new_value in updates.iteritems():
 row[column] = new_value
 # 在表中增加DELETE这个功能很容易：
 def delete(self, predicate=lambda row: True):
"""delete all rows matching predicate
or all rows if no predicate supplied"""
 self.rows = [row for row in self.rows if not(predicate(row))
# 我们会给 Table 类一个 select() 方法来返回一个新 Table。这个方法采用两种可选语句。
#  keep_columns 声明了你希望在结果中保留的列名。如果没提供这一项，结果会包含所有的列。
#  additional_columns 是一个字典，它的键是新列名，值是指定如何计算新列值的函数。
# 如果两种都不用，你只会得到一个表的机械复制的版本：
def select(self, keep_columns=None, additional_columns=None):
if keep_columns is None: # 如果没有指定列
 keep_columns = self.columns # 则返回所有列
if additional_columns is None:
 additional_columns = {}
 # 结果的新表
 result_table = Table(keep_columns + additional_columns.keys())
for row in self.rows:
 new_row = [row[column] for column in keep_columns]
for column_name, calculation in additional_columns.iteritems():
 new_row.append(calculation(row))
 result_table.insert(new_row)
 return result_table
# 我们也需要 where() 和 limit() 方法。两种方法都很简单：
def where(self, predicate=lambda row: True):
"""return only the rows that satisfy the supplied predicate"""
 where_table = Table(self.columns)
 where_table.rows = filter(predicate, self.rows)
return where_table
def limit(self, num_rows):
"""return only the first num_rows rows"""
 limit_table = Table(self.columns)
 limit_table.rows = self.rows[:num_rows]
return limit_table
# 我们增加一个 group_by() 方法。
def group_by(self, group_by_columns, aggregates, having=None):
 grouped_rows = defaultdict(list)
 # 填充组
for row in self.rows:
 key = tuple(row[column] for column in group_by_columns)
 grouped_rows[key].append(row)
 # 结果表中包含组列与汇总
 result_table = Table(group_by_columns + aggregates.keys())
 for key, rows in grouped_rows.iteritems():
if having is None or having(rows):
 new_row = list(key)
for aggregate_name, aggregate_fn in aggregates.iteritems():
 new_row.append(aggregate_fn(rows))
 result_table.insert(new_row)
return result_table
# name_length 标准表示
如下所示：
def min_user_id(rows): return min(row["user_id"] for row in rows)
stats_by_length = users \
 .select(additional_columns={"name_length" : name_length}) \
 .group_by(group_by_columns=["name_length"],
 aggregates={ "min_user_id" : min_user_id,
 "num_users" : len })

# first_letter 的标准表示是：
def first_letter_of_name(row):
 return row["name"][0] if row["name"] else ""
def average_num_friends(rows):
return sum(row["num_friends"] for row in rows) / len(rows)
def enough_friends(rows):
return average_num_friends(rows) > 1
avg_friends_by_letter = users \
 .select(additional_columns={'first_letter' : first_letter_of_name}) \
 .group_by(group_by_columns=['first_letter'],
 aggregates={ "avg_num_friends" : average_num_friends },
 having=enough_friends)
user_id_sum 的标准表示是：
def sum_user_ids(rows): return sum(row["user_id"] for row in rows)
user_id_sum = users \
 .where(lambda row: row["user_id"] > 1) \
 .group_by(group_by_columns=[],
 aggregates={ "user_id_sum" : sum_user_ids })

# 可以通过给表提供一个具有排序（order）功能的 order_by() 方法来轻易实现：
def order_by(self, order):
 new_table = self.select() # 进行一次复制
 new_table.rows.sort(key=order)
 return new_table

# NotQuiteABase 的 join() 实现更为严格一些——它只对两表有共同列的部分做合并。虽然
如此，也不妨把它写出来：
def join(self, other_table, left_join=False):
 join_on_columns = [c for c in self.columns # 两个表的列
if c in other_table.columns] 
 additional_columns = [c for c in other_table.columns # 右表中的列
if c not in join_on_columns]
 # 左表中所有列 + 右表增加的列
 join_table = Table(self.columns + additional_columns)
 for row in self.rows:
def is_join(other_row):
return all(other_row[c] == row[c] for c in join_on_columns)
 other_rows = other_table.where(is_join).rows
 # 每对匹配的行生成一个新行
for other_row in other_rows:
 join_table.insert([row[c] for c in self.columns] +
 [other_row[c] for c in additional_columns])
  # 如果没有行匹配，在左并集的操作下生成空值
if left_join and not other_rows:
 join_table.insert([row[c] for c in self.columns] +
 [None for c in additional_columns])
return join_table

# 获得兴趣的数目：
def count_interests(rows):
"""counts how many rows have non-None interests"""
return len([row for row in rows if row["interest"] is not None])






users = Table(["user_id", "name", "num_friends"])
users.insert([0, "Hero", 0])
users.insert([1, "Dunn", 2])
users.insert([2, "Sue", 3])
users.insert([3, "Chi", 3])
users.insert([4, "Thor", 3])
users.insert([5, "Clive", 2])
users.insert([6, "Hicks", 3])
users.insert([7, "Devin", 2])
users.insert([8, "Kate", 2])
users.insert([9, "Klein", 3])
users.insert([10, "Jen", 1])
print("users : ", users)

# 测试update
users.update({'num_friends' : 3}, # 设定 num_friends = 3
lambda row: row['user_id'] == 1) # 在user_id == 1的行中

# 测试delete
users.delete(lambda row: row["user_id"] == 1) # 删掉user_id == 1的行
users.delete() # 删掉每一行

# 然后我们可以轻松创建与先前的 SQL 语句等价的 NotQuiteABase 语句：
# SELECT * FROM users;
users.select()
# SELECT * FROM users LIMIT 2;
users.limit(2)
# SELECT user_id FROM users;
users.select(keep_columns=["user_id"])
# SELECT user_id FROM users WHERE name = 'Dunn';
users.where(lambda row: row["name"] == "Dunn") \
.select(keep_columns=["user_id"])
# SELECT LENGTH(name) AS name_length FROM users;
def name_length(row): return len(row["name"])
users.select(keep_columns=[],
 additional_columns = { "name_length" : name_length })

# 测试的 order_by() 方法
friendliest_letters = avg_friends_by_letter \
 .order_by(lambda row: -row["avg_num_friends"]) \
 .limit(4)


