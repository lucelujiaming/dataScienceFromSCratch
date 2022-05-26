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

def fix_unicode(text):
	return text.replace(u"\u2019", "'")

# 在获得了网页的文本之后，我们需要把它做成一个由单词和句号组成的序列。
from bs4 import BeautifulSoup
import requests
url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html5lib')
content = soup.find("div", "entry-content") # 找到entry-content div
regex = r"[\w']+|[\.]" # 匹配一个单词或一个句点
document = []
for paragraph in content("p"):
	words = re.findall(regex, fix_unicode(paragraph.text))
	document.extend(words)

# 我们可以利用 zip(document, document[1:]) 求出文档中有多少对连续元素：
bigrams = zip(document, document[1:])
transitions = defaultdict(list)
for prev, current in bigrams:
	transitions[prev].append(current)
# 下面我们就可以生成句子了：
def generate_using_bigrams():
	current = "." # 这意味着下一个单词是一个新句子的开头
	result = []
	while True:
		next_word_candidates = transitions[current] # 双连词 (current, _)
		current = random.choice(next_word_candidates) # 随机选择一个
		result.append(current) # 将其附加到结果中
		if current == ".": return " ".join(result) # 如果是"."，就完成了
		print("result = ", result)
generate_using_bigrams()
# 现在，这种语次转变将取决于前两个单词：
trigrams = zip(document, document[1:], document[2:])
trigram_transitions = defaultdict(list)
starts = []
for prev, current, next in trigrams:
	if prev == ".": # 如果前一个"单词"是个句点
		starts.append(current) # 那么这就是一个起始单词
	trigram_transitions[(prev, current)].append(next)
# 需要注意的是，现在我们必须将这些起始词单独记录下来。
# 我们可以使用几乎相同的方法来生成句子：
def generate_using_trigrams():
	current = random.choice(starts) # 随机选择一个起始单词
	prev = "." # 前面加一个句点'.'
	result = [current]
	while True:
		next_word_candidates = trigram_transitions[(prev, current)]
		next_word = random.choice(next_word_candidates)
		prev, current = current, next_word
		result.append(current)
		if current == ".":
			return " ".join(result)
		print("new result = ", result)
generate_using_trigrams()



