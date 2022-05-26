# coding: utf-8
from my_Bayes import *
from test_split_data import *


import glob, re
# 把路径修改为你存放文件的那个
path = r"/Users/lucelu/Downloads/SpamAssassin/*/*"
data = []
# glob.glob会返回每一个与通配路径所匹配的文件名
for fn in glob.glob(path):
	is_spam = "ham" not in fn
	# with open(fn,'r') as file:
	with open(fn,'r', encoding='latin-1') as file: 
		for line in file:
			if line.startswith("Subject:"):
				# 移除开头的"Subject: "，保留其余内容
				subject = re.sub(r"^Subject: ", "", line).strip()
				data.append((subject, is_spam))

 # 我们把数据分为训练数据和测试数据，然后开始建立分类器：
random.seed(0) # 这样你能得到与我相同的答案
train_data, test_data = split_data(data, 0.75)

classifier = NaiveBayesClassifier()
classifier.train(train_data)

# 然后，我们可以检查一下模型的效果如何：
# 三个元素 (主题，确实是垃圾邮件，预测为垃圾邮件的概率)
classified = [(subject, is_spam, classifier.classify(subject))
			for subject, is_spam in test_data]
# 假设spam_probability > 0.5对应的是预测为垃圾邮件
# 对(actual is_spam, predicted is_spam)的组合计数
from collections import Counter # 默认未加载
counts = Counter((is_spam, spam_probability > 0.5)
			for _, is_spam, spam_probability in classified)

print("counts = ", counts)

#	# 引出了一个有趣的问题，到底哪些邮件最容易被错误分类呢？请看下面的代码：
#	# 根据spam_probability从最小到最大排序
#	classified.sort(key=lambda row: row[2])
#	# 非垃圾邮件被预测为垃圾邮件的最高概率
#	spammiest_hams = filter(lambda row: not row[1], classified)[-5:]
#	# 垃圾邮件被预测为垃圾邮件的最低概率
#	hammiest_spams = filter(lambda row: row[1], classified)[:5]

# 同样，我们也可以看出现哪些词最容易被误判为垃圾邮件，具体代码如下所示：
def p_spam_given_word(word_prob):
	"""uses bayes's theorem to compute p(spam | message contains word)"""
	# word_prob是由word_probabilities生成的三元素中的一个
	word, prob_if_spam, prob_if_not_spam = word_prob
	return prob_if_spam / (prob_if_spam + prob_if_not_spam)
words = sorted(classifier.word_probs, key=p_spam_given_word)
spammiest_words = words[-5:]
hammiest_words = words[:5]

# print("words = ", words)
print("spammiest_words = ", spammiest_words)
print("hammiest_words = ", hammiest_words)


