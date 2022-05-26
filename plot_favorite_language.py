# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from all_cities import *
from plot_state_borders import *

# 键是语言，值是成对数据(longitudes, latitudes)
plots = { "Java" : ([], []), "Python" : ([], []), "R" : ([], []) }

# 根据数据作图，键是语言，值是成对数据(longitudes, latitudes)
# 我们希望每种语言都能有不同的记号和颜色
markers = { "Java" : "o", "Python" : "s", "R" : "^" }
colors = { "Java" : "r", "Python" : "b", "R" : "g" }
for (longitude, latitude), language in all_cities:
	 plots[language][0].append(longitude)
	 plots[language][1].append(latitude)
# 对每种语言创建一个散点序列
# for language, (x, y) in plots.iteritems():
for language, (x, y) in plots.items():
	plt.scatter(x, y, color=colors[language], marker=markers[language],
					  label=language, zorder=10)
plot_state_borders(plt) # 假设我们有一个实现这一步的函数
plt.legend(loc=0) # 让matplotlib选择一个位置
plt.axis([-130,-60,20,55]) # 设置轴
plt.title("最受欢迎的编程语言")
plt.show()



