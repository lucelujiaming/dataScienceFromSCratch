# coding: utf-8

import math
import random

def try_or_none(f):
	"""wraps f to return None if f raises an exception
	assumes f takes only one input"""
	def f_or_none(x):
		try: return f(x)
		except: return None
	return f_or_none

# 列出一系列解析器，每个解析器具体说明其中一列如何解析。
def bad_parse_row(input_row, parsers):
	"""given a list of parsers (some of which may be None)
	apply the appropriate one to each element of the input_row"""
	return [parser(value) if parser is not None else value
			for value, parser in zip(input_row, parsers)]
def parse_row(input_row, parsers):
	return [try_or_none(parser)(value) if parser is not None else value
			for value, parser in zip(input_row, parsers)]
def parse_rows_with(reader, parsers):
	"""wrap a reader to apply the parsers to each of its rows"""
	for row in reader:
	 	yield parse_row(row, parsers)

import dateutil.parser
import csv
data = []
# with open("comma_delimited_stock_prices.csv", "rb") as f:
with open("comma_delimited_stock_prices.csv", "r") as f:
	reader = csv.reader(f)
	for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
		data.append(line)
for row in data:
	if any(x is None for x in row):
		print(row)

# 为csv.DictReader 创建相似的帮助函数。
# 这样的话，你很可能希望提供基于域名的解析字典。例如：
def try_parse_field(field_name, value, parser_dict):
	"""try to parse value using the appropriate function from parser_dict"""
	parser = parser_dict.get(field_name) # 如果没有此条目，则为None
	if parser is not None:
		return try_or_none(parser)(value)
	else:
		return value
def parse_dict(input_dict, parser_dict):
	return { field_name : try_parse_field(field_name, value, parser_dict)
			for field_name, value in input_dict.iteritems() }







