# coding: utf-8
from my_linear_algebra import *
import math
import random

# 把导数看成是其第 i 个变量的函数，其他变量保持不变，以此来计算它第 i 个偏导数：
def partial_difference_quotient(f, v, i, h):
	"""compute the ith partial difference quotient of f at v"""
	w = [v_j + (h if j == i else 0) # 只对v的第i个元素增加h
			for j, v_j in enumerate(v)]
	return (f(w) - f(v)) / h

# 再以同样的方法估算它的梯度函数：
# 使用枚举（enumerate）产生 (index, element) 元组
def estimate_gradient(f, v, h=0.00001):
	return [partial_difference_quotient(f, v, i, h)
				for i, _ in enumerate(v)]

# 用梯度方法从所有的三维向量中找到最小值。
def step(v, direction, step_size):
	"""move step_size in the direction from v"""
	return [v_i + step_size * direction_i
		for v_i, direction_i in zip(v, direction)]

def sum_of_squares_gradient(v):
	return [2 * v_i for v_i in v]

# 选取一个随机初始值
v = [random.randint(-10,10) for i in range(3)]
tolerance = 0.0000001
while True:
	gradient = sum_of_squares_gradient(v) # 计算v的梯度
	next_v = step(v, gradient, -0.01) # 取负的梯度步长
	if distance(next_v, v) < tolerance: # 如果收敛了就停止
		break
	v = next_v # 如果没汇合就继续

# print("v : ", v)

#  创建一个对无效输入值返回无限值
# （即这个值永远不会成为任何函数的最小值）的“安全应用”函数：
def safe(f):
	"""return a new function that's the same as f,
	   except that it outputs infinity whenever f produces an error"""
	def safe_f(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except:
			return float('inf') # 意思是Python中的“无限值”
	return safe_f

# 第一版梯度下降法：
def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
	"""use gradient descent to find theta that minimizes target function"""
	step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
	theta = theta_0               # 设定theta为初始值
	target_fn = safe(target_fn)   # target_fn的安全版
	value = target_fn(theta)      # 我们试图最小化的值
	# 在每一步梯度计算中，它都会搜索整个数据集。
	while True:
		gradient = gradient_fn(theta)
		next_thetas = [step(theta, gradient, - step_size)
				for step_size in step_sizes]
	# 选择一个使残差函数最小的值
	next_theta = min(next_thetas, key=target_fn)
	next_value = target_fn(next_theta)
	# 当“收敛”时停止
	if abs(value - next_value) < tolerance:
		return theta
	else:
 		theta, value = next_theta, next_value

# 需要最大化某个函数，这只需要最小化这个函数的负值
def negate(f):
	"""return a function that for any input x returns -f(x)"""
	return lambda *args, **kwargs: -f(*args, **kwargs)
def negate_all(f):
	"""the same when f returns a list of numbers"""
	return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]
def maximize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
	return minimize_batch(negate(target_fn),
			 negate_all(gradient_fn),
			 theta_0,
			 tolerance)

# 随机梯度下降（stochastic gradient descent）的技术，
# 它每次仅计算一个点的梯度（并向前跨一步）。这个计算会反复循环，直到达到一个停止点。
# 在每个循环中，我们都会在整个数据集上按照一个随机序列迭代：
def in_random_order(data):
	"""generator that returns the elements of data in random order"""
	indexes = [i for i, _ in enumerate(data)] # 生成索引列表
	random.shuffle(indexes) # 随机打乱数据
	for i in indexes: # 返回序列中的数据
		yield data[i]

# 第二版梯度下降法：
def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
	data = zip(x, y)
	theta = theta_0                             # 初始值猜测
	alpha = alpha_0                             # 初始步长
	min_theta, min_value = None, float("inf")   # 迄今为止的最小值
	iterations_with_no_improvement = 0

	# 如果循环超过100次仍无改进，停止
	while iterations_with_no_improvement < 100:
		value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )
		if value < min_value:
			# 如果找到新的最小值，记住它
			# 并返回到最初的步长
			min_theta, min_value = theta, value
			iterations_with_no_improvement = 0
			alpha = alpha_0
		else:
			# 尝试缩小步长，否则没有改进
			iterations_with_no_improvement += 1
			alpha *= 0.9
		# 在每个数据点上向梯度方向前进一步
		for x_i, y_i in in_random_order(data):
			gradient_i = gradient_fn(x_i, y_i, theta)
			theta = vector_subtract(theta, 
				scalar_multiply(alpha, gradient_i))
	return min_theta

# 我们也希望获得最大化的结果：
def maximize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
	return minimize_stochastic(negate(target_fn),
				 negate_all(gradient_fn),
				 x, y, theta_0, alpha_0)
