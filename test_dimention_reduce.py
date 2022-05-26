# coding: utf-8

from my_linear_algebra  import *
from test_adjusted_data import *
from test_gradient_descent import *

# 将数据转换成前N个主成分的伪码大致如下：
#   1. 去除平均值
#   2. 计算协方差矩阵
#   3. 计算协方差矩阵的特征值和特征向量
#   4. 将特征值从大到小排序
#   5. 保留最上面的N个特征向量
#   6. 将数据转换到上述N个特征向量构建的新空间中

test_w = make_matrix(5, 5, random_value)
test_data = make_matrix(5, 5, random_value)
# 将数据转换成为每个维度均值为零的形式：
def de_mean_matrix(A):
	"""returns the result of subtracting from every value in A the mean
	value of its column. the resulting matrix has mean 0 in every column"""
	nr, nc = shape(A)
	column_means, _ = scale(A)
	return make_matrix(nr, nc, 
			lambda i, j: A[i][j] - column_means[j])
# 已有一个去均值的矩阵 X
test_X = de_mean_matrix(test_data)
print("de_mean_matrix : ", test_X)

# 抓住数据最大变差的方向
# 给定一个方向d（一个绝对值为1的向量），
# 矩阵的每行x在方向d的扩展是点积dot(x,d)。函数magnitude执行该操作。
# 并且如果将每个非零向量w的绝对值大小调整为1，则它们每个都决定了一个方向：
def direction(w):
	# 计算向量的大小（或长度）：
	mag = magnitude(w)
	# 绝对值大小调整为1
	return [w_i / mag for w_i in w]
print(test_w[0])
print("direction : ", direction(test_w[0]))

# 因此，已知一个非零向量 w，我们可以计算 w 方向上的方差：
def directional_variance_i(x_i, w):
	"""the variance of the row x_i in the direction determined by w"""
	return dot(x_i, direction(w)) ** 2
def directional_variance(X, w):
	"""the variance of the data in the direction determined w"""
	return sum(directional_variance_i(x_i, w)
				for x_i in X)
print("directional_variance : ", 
	directional_variance(test_X, test_w[0]))

# 只要得到梯度函数，我们就可以通过梯度下降法计算出来：
def directional_variance_gradient_i(x_i, w):
	"""the contribution of row x_i to the gradient of
	   the direction-w variance"""
	projection_length = dot(x_i, direction(w))
	return [2 * projection_length * x_ij for x_ij in x_i]
def directional_variance_gradient(X, w):
	return vector_sum(directional_variance_gradient_i(x_i,w)
					for x_i in X)
print("directional_variance_gradient : ", 
	directional_variance_gradient(test_X, test_w[0]))

# 第一主成分仅是使函数 directional_variance 最大化的方向：
from functools import partial
def first_principal_component(X):
	guess = [1 for _ in X[0]]
	unscaled_maximizer = maximize_batch(
		partial(directional_variance, X),          # 现在是w的一个函数
		partial(directional_variance_gradient, X), # 现在是w的一个函数
		guess)
	return direction(unscaled_maximizer)
# 执行起来非常慢。因为maximize_batch使用的是每次搜索整个数据集的方法。
# print("first_principal_component : ", 
#	first_principal_component(test_X))

# 也许，你也有可能使用随机梯度下降方法：
# 这里没有"y"，所以我们仅仅是传递一个Nones的向量和忽略这个输入的函数
def first_principal_component_sgd(X):
	guess = [1 for _ in X[0]]
	unscaled_maximizer = maximize_stochastic(
			lambda x, _, w: directional_variance_i(x, w),
			lambda x, _, w: directional_variance_gradient_i(x, w),
			X,
			[None for _ in X], # 假的 "y"
			guess)
	return direction(unscaled_maximizer)
v_direction = first_principal_component_sgd(test_X)
print("first_principal_component_sgd : ", v_direction)

# 将数据在这个方向上投影得到这个成分的值：
def project(v, w):
	"""return the projection of v onto the direction w"""
	projection_length = dot(v, w)
	return scalar_multiply(projection_length, w)
print("project : ", project(v_direction, test_w[0]))


# 如果还想得到其他的成分，就要先从数据中移除投影：
def remove_projection_from_vector(v, w):
	"""projects v onto w and subtracts the result from v"""
	return vector_subtract(v, project(v, w))
def remove_projection(X, w):
	"""for each row of X
	projects the row onto w, and subtracts the result from the row"""
	return [remove_projection_from_vector(x_i, w) for x_i in X]
print("remove_projection : ", remove_projection(test_X, test_w[0]))

# 在更高维的数据集中，我们可以通过迭代找到我们所需的任意数目的主成分：
def principal_component_analysis(X, num_components):
	components = []
	for _ in range(num_components):
		# component = first_principal_component(X)
		component = first_principal_component_sgd(X)
		components.append(component)
		X = remove_projection(X, component)
	return components
components_ret = principal_component_analysis(test_X, 5)
print("principal_component_analysis : ", components_ret)
# 然后再将原数据转换为由主成分生成的低维空间中的点：
def transform_vector(v, components):
	return [dot(v, w) for w in components]
def transform(X, components):
	return [transform_vector(x_i, components) for x_i in X]
reconMat = transform(test_X, components_ret)
print("transform : ", reconMat)




