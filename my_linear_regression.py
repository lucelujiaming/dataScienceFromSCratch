# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
import math
import random

# 线性关系预测函数：
def predict(alpha, beta, x_i):
	return beta * x_i + alpha

# 计算它们的误差：
def error(alpha, beta, x_i, y_i):
	"""the error from predicting beta * x_i + alpha
	when the actual value is y_i"""
	return y_i - predict(alpha, beta, x_i)

# 对误差的平方求和：
def sum_of_squared_errors(alpha, beta, x, y):
	return sum(error(alpha, beta, x_i, y_i) ** 2
				for x_i, y_i in zip(x, y))

# 利用微积分（或单调乏味的代数），我们就可以求出令误差最小化的 alpha 和 beta 了：
def least_squares_fit(x, y):
	"""given training values for x and y,
	find the least-squares values of alpha and beta"""
	beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
	alpha = mean(y) - beta * mean(x)
	return alpha, beta

# 使用第 5 章中的异常值数据来计算这两个值：
alpha, beta = least_squares_fit(num_friends_good, daily_minutes_good)
# print(alpha, beta)

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

evaluate_data_good = [ beta * num_friend + alpha for num_friend in num_friends_good]

# print(len(num_friends_good), len(daily_minutes_good), len(evaluate_data_good))

# plt.scatter(num_friends_good,daily_minutes_good)
# plt.scatter(num_friends_good,evaluate_data_good)
# plt.show()

# 决定系数（coefficient of determination）或 R 平方，
# 用来表示纳入模型的自变量引起的变动占总变动的百分比：
def total_sum_of_squares(y):
	"""the total squared variation of y_i's from their mean"""
	return sum(v ** 2 for v in de_mean(y))
def r_squared(alpha, beta, x, y):
	"""the fraction of variation in y captured by the model, which equals
	1 - the fraction of variation in y not captured by the model"""
	return 1.0 - (sum_of_squared_errors(alpha, beta, x, y) /
				  total_sum_of_squares(y))

r_squared_ret = r_squared(alpha, beta, num_friends_good, daily_minutes_good) # 0.329
# print(r_squared_ret)

# 通过梯度下降法来求参数：
def squared_error(x_i, y_i, theta):
	alpha, beta = theta
	return error(alpha, beta, x_i, y_i) ** 2
def squared_error_gradient(x_i, y_i, theta):
	alpha, beta = theta
	return [-2 * error(alpha, beta, x_i, y_i), # alpha偏导数
 			-2 * error(alpha, beta, x_i, y_i) * x_i] # beta偏导数
# 选择一个随机值作为开始
random.seed(0)
theta = [random.random(), random.random()]
alpha, beta = minimize_stochastic(squared_error,
				squared_error_gradient,
				num_friends_good,
				daily_minutes_good,
				theta,
				0.0001)
# 好像不太对。。
# print(alpha, beta)



