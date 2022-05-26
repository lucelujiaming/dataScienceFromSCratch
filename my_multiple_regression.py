# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_linear_regression import *

import math
import random

# 我们的模型可以用下列函数实现：
def predict(x_i, beta):
	"""assumes that the first element of each x_i is 1"""
	return dot(x_i, beta)

# 要单次预测对应的平方误差：
def error(x_i, y_i, beta):
	return y_i - predict(x_i, beta)
def squared_error(x_i, y_i, beta):
	return error(x_i, y_i, beta) ** 2
# 如果你熟悉微积分，可以通过下面的方式进行计算：
def squared_error_gradient(x_i, y_i, beta):
	"""the gradient (with respect to beta)
	corresponding to the ith squared error term"""
	return [-2 * x_ij * error(x_i, y_i, beta)
				for x_ij in x_i]

# 利用随机梯度下降法来寻找最优的 beta：
random.seed(0)
def estimate_beta(x, y):
	beta_initial = [random.random() for x_i in x[0]]
	return minimize_stochastic(squared_error,
		squared_error_gradient,
		x, y,
		beta_initial,
		0.001)

# beta = estimate_beta(x, daily_minutes_good) # [30.63, 0.972, -1.868, 0.911]

# 我们再来看看 R 的平方值，目前已经升至 0.68 了：
def multiple_r_squared(x, y, beta):
	sum_of_squared_errors = sum(error(x_i, y_i, beta) ** 2
							for x_i, y_i in zip(x, y))
	return 1.0 - sum_of_squared_errors / total_sum_of_squares(y)

# 利用 Bootstrap 来获得新的数据集，
# 即选择 n 个数据点并用原来的数据将其替换，然后计算合成的数据集的中位数：
def bootstrap_sample(data):
	"""randomly samples len(data) elements with replacement"""
	return [random.choice(data) for _ in data]
def bootstrap_statistic(data, stats_fn, num_samples):
	"""evaluates stats_fn on num_samples bootstrap samples from data"""
	return [stats_fn(bootstrap_sample(data))
					for _ in range(num_samples)]

# 例如，考虑下列两个数据集：
# 101个点都非常接近100
close_to_100 = [99.5 + random.random() for _ in range(101)]
# 101个点钟，50个接近0，50个接近200
far_from_100 = ([99.5 + random.random()] +
			[random.random() for _ in range(50)] +
			[200 + random.random() for _ in range(50)])

# 如果你考察下面的语句，大部分情况下你看到的数字确实非常接近 100。：
bootstrap_statistic(close_to_100, median, 100)
# 然而，如果你考察下面的语句。
# 你会发现，不仅有许多数字接近 0，而且还有许多数字接近 200。
bootstrap_statistic(far_from_100, median, 100)

# 重新组合成一个 x_sample 和一个 y_sample：
def estimate_sample_beta(sample):
	"""sample is a list of pairs (x_i, y_i)"""
	x_sample, y_sample = zip(*sample) # 魔法般的解压方式
	return estimate_beta(x_sample, y_sample)

x = [[1,49,4,0],[1,41,9,0],[1,40,8,0],[1,25,6,0],[1,21,1,0],[1,21,0,0],[1,19,3,0],[1,19,0,0],[1,18,9,0],[1,18,8,0],[1,16,4,0],[1,15,3,0],[1,15,0,0],[1,15,2,0],[1,15,7,0],[1,14,0,0],[1,14,1,0],[1,13,1,0],[1,13,7,0],[1,13,4,0],[1,13,2,0],[1,12,5,0],[1,12,0,0],[1,11,9,0],[1,10,9,0],[1,10,1,0],[1,10,1,0],[1,10,7,0],[1,10,9,0],[1,10,1,0],[1,10,6,0],[1,10,6,0],[1,10,8,0],[1,10,10,0],[1,10,6,0],[1,10,0,0],[1,10,5,0],[1,10,3,0],[1,10,4,0],[1,9,9,0],[1,9,9,0],[1,9,0,0],[1,9,0,0],[1,9,6,0],[1,9,10,0],[1,9,8,0],[1,9,5,0],[1,9,2,0],[1,9,9,0],[1,9,10,0],[1,9,7,0],[1,9,2,0],[1,9,0,0],[1,9,4,0],[1,9,6,0],[1,9,4,0],[1,9,7,0],[1,8,3,0],[1,8,2,0],[1,8,4,0],[1,8,9,0],[1,8,2,0],[1,8,3,0],[1,8,5,0],[1,8,8,0],[1,8,0,0],[1,8,9,0],[1,8,10,0],[1,8,5,0],[1,8,5,0],[1,7,5,0],[1,7,5,0],[1,7,0,0],[1,7,2,0],[1,7,8,0],[1,7,10,0],[1,7,5,0],[1,7,3,0],[1,7,3,0],[1,7,6,0],[1,7,7,0],[1,7,7,0],[1,7,9,0],[1,7,3,0],[1,7,8,0],[1,6,4,0],[1,6,6,0],[1,6,4,0],[1,6,9,0],[1,6,0,0],[1,6,1,0],[1,6,4,0],[1,6,1,0],[1,6,0,0],[1,6,7,0],[1,6,0,0],[1,6,8,0],[1,6,4,0],[1,6,2,1],[1,6,1,1],[1,6,3,1],[1,6,6,1],[1,6,4,1],[1,6,4,1],[1,6,1,1],[1,6,3,1],[1,6,4,1],[1,5,1,1],[1,5,9,1],[1,5,4,1],[1,5,6,1],[1,5,4,1],[1,5,4,1],[1,5,10,1],[1,5,5,1],[1,5,2,1],[1,5,4,1],[1,5,4,1],[1,5,9,1],[1,5,3,1],[1,5,10,1],[1,5,2,1],[1,5,2,1],[1,5,9,1],[1,4,8,1],[1,4,6,1],[1,4,0,1],[1,4,10,1],[1,4,5,1],[1,4,10,1],[1,4,9,1],[1,4,1,1],[1,4,4,1],[1,4,4,1],[1,4,0,1],[1,4,3,1],[1,4,1,1],[1,4,3,1],[1,4,2,1],[1,4,4,1],[1,4,4,1],[1,4,8,1],[1,4,2,1],[1,4,4,1],[1,3,2,1],[1,3,6,1],[1,3,4,1],[1,3,7,1],[1,3,4,1],[1,3,1,1],[1,3,10,1],[1,3,3,1],[1,3,4,1],[1,3,7,1],[1,3,5,1],[1,3,6,1],[1,3,1,1],[1,3,6,1],[1,3,10,1],[1,3,2,1],[1,3,4,1],[1,3,2,1],[1,3,1,1],[1,3,5,1],[1,2,4,1],[1,2,2,1],[1,2,8,1],[1,2,3,1],[1,2,1,1],[1,2,9,1],[1,2,10,1],[1,2,9,1],[1,2,4,1],[1,2,5,1],[1,2,0,1],[1,2,9,1],[1,2,9,1],[1,2,0,1],[1,2,1,1],[1,2,1,1],[1,2,4,1],[1,1,0,1],[1,1,2,1],[1,1,2,1],[1,1,5,1],[1,1,3,1],[1,1,10,1],[1,1,6,1],[1,1,0,1],[1,1,8,1],[1,1,6,1],[1,1,4,1],[1,1,9,1],[1,1,9,1],[1,1,4,1],[1,1,2,1],[1,1,9,1],[1,1,0,1],[1,1,8,1],[1,1,6,1],[1,1,1,1],[1,1,1,1],[1,1,5,1]]
daily_minutes_good = [68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]
random.seed(0) # so that you get the same results as me

bootstrap_betas = bootstrap_statistic(list(zip(x, daily_minutes_good)),
                                      estimate_sample_beta,
                                      100)
# 之后，我们就可以估算每个系数的标准偏差了：
bootstrap_standard_errors = [
		standard_deviation([beta[i] for beta in bootstrap_betas])
		for i in range(4)]
# [1.174, # 常数项， 实际误差 = 1.19
# 0.079, # num_friends， 实际误差 = 0.080
# 0.131, # unemployed, 实际误差 = 0.127
# 0.990] # phd, 实际误差 = 0.998

# 使用 normal_cdf 了，并且我们觉得它效果还不错：
from inverse_normal_cdf import *
def p_value(beta_hat_j, sigma_hat_j):
	if beta_hat_j > 0:
		# 如果系数是正的，则我们需要对
		# 看见一个更大的值的概率做两次计算
		return 2 * (1 - normal_cdf(beta_hat_j / sigma_hat_j))
	else:
		# 否则看见一个更小值的概率乘以2
		return 2 * normal_cdf(beta_hat_j / sigma_hat_j)
# print(p_value(30.63, 1.174)) # ~0 (常数项)
# print(p_value(0.972, 0.079)) # ~0 (num_friends)
# print(p_value(-1.868, 0.131)) # ~0 (work_hours)
# print(p_value(0.911, 0.990)) # 0.36 (phd)

# 在岭回归（ridge regression）中，
# 我们添加了一个与 beta_i 的平方之和成正比的惩罚项。
# alpha是一个*超参数*，用来控制惩罚的程度
# 它有时被叫作"lambda"，但这在Python中另有所指
def ridge_penalty(beta, alpha):
	return alpha * dot(beta[1:], beta[1:])
def squared_error_ridge(x_i, y_i, beta, alpha):
	"""estimate error plus ridge penalty on beta"""
	return error(x_i, y_i, beta) ** 2 + ridge_penalty(beta, alpha)
# 之后你可以按通常的方法插入梯度下降：
def ridge_penalty_gradient(beta, alpha):
	"""gradient of just the ridge penalty"""
	return [0] + [2 * alpha * beta_j for beta_j in beta[1:]]
def squared_error_ridge_gradient(x_i, y_i, beta, alpha):
	"""the gradient corresponding to the ith squared error term
	including the ridge penalty"""
	return vector_add(squared_error_gradient(x_i, y_i, beta),
					  ridge_penalty_gradient(beta, alpha))
def estimate_beta_ridge(x, y, alpha):
	"""use gradient descent to fit a ridge regression
	with penalty alpha"""
	beta_initial = [random.random() for x_i in x[0]]
	return minimize_stochastic(partial(squared_error_ridge, alpha=alpha),
							partial(squared_error_ridge_gradient,
							alpha=alpha),
							x, y,
							beta_initial,
							0.001)
# 如果令 alpha 为 0，则根本不会实施任何惩罚，这时得到的结果跟前面一样：
from functools import partial
beta_0 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.0)
# [30.6, 0.97, -1.87, 0.91]
# print(dot(beta_0[1:], beta_0[1:])) # 5.26
# print(multiple_r_squared(x, daily_minutes_good, beta_0)) # 0.680
# 随着 alpha 的增大，拟合优度会变差，但是 beta 会变小：
beta_0_01 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.01)
# print(beta_0_01)

# [30.6, 0.97, -1.86, 0.89]
# print(dot(beta_0_01[1:], beta_0_01[1:])) # 5.19
# print(multiple_r_squared(x, daily_minutes_good, beta_0_01)) # 0.680
beta_0_1 = estimate_beta_ridge(x, daily_minutes_good, alpha=0.1)
# print(beta_0_01)

# [30.8, 0.95, -1.84, 0.54]
# print(dot(beta_0_1[1:], beta_0_1[1:])) # 4.60
# print(multiple_r_squared(x, daily_minutes_good, beta_0_1)) # 0.680
beta_1 = estimate_beta_ridge(x, daily_minutes_good, alpha=1)
# print(beta_0_01)

# [30.7, 0.90, -1.69, 0.085]
# print(dot(beta_1[1:], beta_1[1:])) # 3.69
# print(multiple_r_squared(x, daily_minutes_good, beta_1)) # 0.676
beta_10 = estimate_beta_ridge(x, daily_minutes_good, alpha=10)
# print(beta_0_01)

# [28.3, 0.72, -0.91, -0.017]
# print(dot(beta_10[1:], beta_10[1:])) # 1.36
# print(multiple_r_squared(x, daily_minutes_good, beta_10)) # 0.573
# print(beta_0_01)

# 还有一个方法是 lasso 回归，它用的惩罚方式如下所示：
def lasso_penalty(beta, alpha):
	return alpha * sum(abs(beta_i) for beta_i in beta[1:])





