# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

friends = [ 70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
plt.scatter(friends, minutes)
# 每个点加标记
for label, friend_count, minute_count in zip(labels, friends, minutes):
	plt.annotate(label,
		xy=(friend_count, minute_count), # 把标记放在对应的点上
		xytext=(5, -5), # 但要有轻微偏离
		textcoords='offset points')
plt.title("日分钟数与朋友数")
plt.xlabel("朋友数")
plt.ylabel("花在网站上的日分钟数")
plt.show()