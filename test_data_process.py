# coding: utf-8

import math
import random
import datetime

data = [
 {'closing_price': 102.06,
 'date': datetime.datetime(2014, 8, 29, 0, 0),
 'symbol': 'AAPL'},
 # ...
]

# 将这个工作分解成具体的步骤：
# 	 (1) 将数据限定在 AAPL 行上；
# 	 (2) 从每行提取收盘价 closing_price；
# 	 (3) 取价格中的最大值 max。
# 我们可以使用一个列表解析一次性完成这三个步骤：
max_aapl_price = max(row["closing_price"]
			for row in data
			if row["symbol"] == "AAPL")

# 知道数据集中每只股票的最高收盘价。
# (1) 聚集起股票代码（symbol）相同的行。
# (2) 在每组中，重复之前的工作：
# 按股票代码对行分组
from collections import defaultdict
by_symbol = defaultdict(list)
for row in data:
 by_symbol[row["symbol"]].append(row)
# 使用字典解析找到每个股票代码的最大值max(row["closing_price"])
max_price_by_symbol = { symbol : max(row["closing_price"]
			for row in grouped_rows)
				# for symbol, grouped_rows in by_symbol.iteritems() }
				for symbol, grouped_rows in by_symbol.items() }

# 创建一个函数，以从字典中提取一个字段，
def picker(field_name):
	"""returns a function that picks a field out of a dict"""
	return lambda row: row[field_name]
# 创建另一个函数，以从字典集合中提取出同样的字段。
def pluck(field_name, rows):
	"""turn a list of dicts into the list of field_name values"""
	return map(picker(field_name), rows)

# 建立一个函数，通过 group 函数的结果把行分组，
# 并选择性地对每组使用value_transform 函数：
def group_by(grouper, rows, value_transform=None):
	# 键是分组情况的输出，值是行的列表
	grouped = defaultdict(list)
	# 通过 group 函数的结果把行分组
	# 建立一个集合，Key是grouper返回的行元素值，value是行。
	for row in rows:
		grouped[grouper(row)].append(row)
	if value_transform is None:
		return grouped
	else:
		# 选择性地对每组使用value_transform 函数。
		return { key : value_transform(rows)
				# for key, rows in grouped.iteritems() }
				for key, rows in grouped.items() }

# 更简单地再现先前的例子。比如：
max_price_by_symbol = group_by(picker("symbol"),
				data,
				lambda rows: max(pluck("closing_price", rows)))

# 是按照符号将价格分组，再在每组中：
#    (1) 按照日期排列价格；
#    (2) 通过命令 zip 得到配对价格（前一天的，今天的）；
#    (3) 将配对价格转换为新的“百分比变动”行。
# 我们首先写一个函数，来完成每一组内的工作：
def percent_price_change(yesterday, today):
	return today["closing_price"] / yesterday["closing_price"] - 1
def day_over_day_changes(grouped_rows):
	# 按日期对行排序
	ordered = sorted(grouped_rows, key=picker("date"))
	# 对偏移量应用zip函数得到连续两天的成对表示
	return [{ "symbol" : today["symbol"],
				"date" : today["date"],
				"change" : percent_price_change(yesterday, today) }
			for yesterday, today in zip(ordered, ordered[1:])]
# 然后我们可以将它作为 value_transform 在 group_by 中使用：
# 键是股票代码，值是一个"change"字典的列表
changes_by_symbol = group_by(picker("symbol"), data, day_over_day_changes)
# 收集所有"change"字典放入一个大列表中
all_changes = [change
			for changes in changes_by_symbol.values()
			for change in changes]

# 找到最大值与最小值：
#	# print("max : ", max(all_changes, key=picker("change")))
#	print("max : ", max(list(all_changes), key=picker("change")), default=0)
#	# print("min : ", min(all_changes, key=picker("change")))
#	print("min : ", min(list(all_changes), key=picker("change")))

# 写一个恰当的 value_transform 函数，然后使用 group_by 函数：
# 为了组合百分比的变化，我们对每一项加1，把它们相乘，再减去1
# 比如，如果我们组合 +10% 和 -20%, 总体的改变是
# (1 + 10%) * (1 - 20%) - 1 = 1.1 * .8 - 1 = -12%
def combine_pct_changes(pct_change1, pct_change2):
	return (1 + pct_change1) * (1 + pct_change2) - 1
from functools import reduce
def overall_change(changes):
	return reduce(combine_pct_changes, pluck("change", changes))

overall_change_by_month = group_by(lambda row: row['date'].month,
										all_changes,
										overall_change)
