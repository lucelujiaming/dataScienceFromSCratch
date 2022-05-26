# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 一个有误导性 y 轴的条形图
mentions = [500, 505]
years = [2013, 2014]

plt.bar([2012.6, 2013.6], mentions, 0.8)
plt.xticks(years)
plt.ylabel("听到有人提及‘数据科学’的次数")

# 如果不这么做，matplotlib会把x轴的刻度标记为0和1
# 然后会在角上加上+2.013e3（糟糕的matplotlib操作！）
plt.ticklabel_format(useOffset=False)
# 这会误导y轴只显示500以上的部分
plt.axis([2012.5,2014.5,499,506])
plt.title("快看如此'巨大'的增长！")
plt.show()

plt.bar([2012.6, 2013.6], mentions, 0.8)
plt.xticks(years)
plt.ylabel("听到有人提及‘数据科学’的次数")

# 如果不这么做，matplotlib会把x轴的刻度标记为0和1
# 然后会在角上加上+2.013e3（糟糕的matplotlib操作！）
plt.ticklabel_format(useOffset=False)
# 使用了一种更合理的轴，这样它看起来就不那么异常了：
plt.axis([2012.5,2014.5,0,550])
plt.title("增长不那么巨大了")
plt.show()
