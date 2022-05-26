# coding: utf-8

from my_linear_algebra import *
from inverse_normal_cdf import *

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i, j)th entry
    is the correlation between columns i and j of data"""
    _, num_columns = shape(data)
    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))
    return make_matrix(num_columns, num_columns, matrix_entry)

data = make_matrix(5, 5, is_diagonal)
_, num_columns = shape(data)
fig, ax = plt.subplots(num_columns, num_columns)
for i in range(num_columns):
    for j in range(num_columns):
        # x轴上column_j对y轴上column_i的散点
        if i != j: 
            ax[i][j].scatter(get_column(data, j), get_column(data, i))
        # 只有当 i == j时显示序列名
        else: 
            ax[i][j].annotate("series " + str(i), (0.5, 0.5),
                            xycoords='axes fraction',
                            ha="center", va="center")
        # 除了图的左侧和下方之外，隐藏图的标记
        if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
        if j > 0: ax[i][j].yaxis.set_visible(False)

# 修复右下方和左上方的图标记
# 因为它们只有文本，是错误的
ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
ax[0][0].set_ylim(ax[0][1].get_ylim())
plt.show()

