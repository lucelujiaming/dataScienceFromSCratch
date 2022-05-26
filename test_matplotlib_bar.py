# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 绘制条形图
movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]
# 条形的默认宽度是0.8，因此我们对左侧坐标加上0.1
# 这样每个条形就被放置在中心了
xs = [i + 0.1 for i, _ in enumerate(movies)]
# 使用左侧x坐标[xs]和高度[num_oscars]画条形图
plt.bar(xs, num_oscars)
plt.ylabel("所获奥斯卡金像奖数量")
plt.title("我最喜爱的电影")
# 使用电影的名字标记x轴，位置在x轴上条形的中心
plt.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)
plt.show()

# 绘制拥有大量数值取值的变量直方图，以此来探索这些取值是如何分布的。
from collections import Counter # 默认未加载
grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]
decile = lambda grade: grade // 10 * 10
histogram = Counter(decile(grade) for grade in grades)
plt.bar([x - 4 for x in histogram.keys()], # 每个条形向左侧移动4个单位
        histogram.values(),                # 给每个条形设置正确的高度
        8)                                 # 每个条形的宽度设置为8
plt.axis([-5, 105, 0, 5]) # x轴取值从-5到105
 # y轴取值0到5
plt.xticks([10 * i for i in range(11)]) # x轴标记为0，10，...，100
plt.xlabel("十分相")
plt.ylabel("学生数")
plt.title("考试分数分布图")
plt.show()