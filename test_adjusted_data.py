# coding: utf-8

from test_statistics import *

# 对每列计算均值和标准差：
def scale(data_matrix):
    """returns the means and standard deviations of each column"""
    num_rows, num_cols = shape(data_matrix)
    means = [mean(get_column(data_matrix,j))
                for j in range(num_cols)]
    stdevs = [standard_deviation(get_column(data_matrix,j))
                for j in range(num_cols)]
    return means, stdevs
# 然后用结果创建新的数据矩阵：
def rescale(data_matrix):
    """rescales the input data so that each column
    has mean 0 and standard deviation 1
    leaves alone columns with no deviation"""
    means, stdevs = scale(data_matrix)
    def rescaled(i, j):
        if stdevs[j] > 0:
            return (data_matrix[i][j] - means[j]) / stdevs[j]
        else:
            return data_matrix[i][j]
    num_rows, num_cols = shape(data_matrix)
    return make_matrix(num_rows, num_cols, rescaled)

# data = make_matrix(5, 5, random_value)
# print(scale(data))
# print(rescale(data))
