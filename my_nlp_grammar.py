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

# 下面，我们将定义一个稍微复杂的语法：
grammar = {
		"_S" : ["_NP _VP"],
		"_NP" : ["_N",
		"_A _NP _P _A _N"],
		"_VP" : ["_V",
		"_V _NP"],
		"_N" : ["data science", "Python", "regression"],
		"_A" : ["big", "linear", "logistic"],
		"_P" : ["about", "near"],
		"_V" : ["learns", "trains", "tests", "is"]
	}

# 首先，我们需要创建一个简单的辅助函数来识别终端符号：
def is_terminal(token):
	return token[0] != "_"

# 接下来，我们需要编写一个函数，将一个标记列表变成一个句子。
def expand(grammar, tokens):
	for i, token in enumerate(tokens):
		# 跳过终端符号
		if is_terminal(token): continue
		# 如果这一步我们发现了一个非终端符号
		# 需要随机选择一个替代者
		replacement = random.choice(grammar[token]) 
		if is_terminal(replacement):
			tokens[i] = replacement
		else:
			tokens = tokens[:i] + replacement.split() + tokens[(i+1):]
		# 现在展开新的符号列表
		return expand(grammar, tokens)
	# 如果到达这一步，就找出了所有的终端符号，可以收工了
	return tokens
# 现在我们可以生成句子了：
def generate_sentence(grammar):
	return expand(grammar, ["_S"])

tokens = generate_sentence(grammar)
print("tokens = ", tokens)


