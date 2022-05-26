# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *

import math
import random
from collections import defaultdict


# 感知器（perception）可能是最简单的神经网络
def step_function(x):
	return 1 if x >= 0 else 0
def perceptron_output(weights, bias, x):
	"""returns 1 if the perceptron 'fires', 0 if not"""
	calculation = dot(weights, x) + bias
	return step_function(calculation)

# sigmoid 函数。
def sigmoid(t):
	return 1 / (1 + math.exp(-t))

# 这样，我们就能计算其输出了，代码如下所示：
def neuron_output(weights, inputs):
	return sigmoid(dot(weights, inputs))

# 有了这种表示方法，神经网络用起来就会非常简便：
def feed_forward(neural_network, input_vector):
	"""takes in a neural network
	(represented as a list of lists of lists of weights)
	and returns the output from forward-propagating the input"""
	outputs = []
	# 每次处理一层
	for layer in neural_network:
		input_with_bias = input_vector + [1] # 增加一个偏倚输入
		output = [neuron_output(neuron, input_with_bias) # 计算输出
		for neuron in layer] # 每一个神经元
		outputs.append(output) # 记住它
		# 然后下一层的输入就是这一层的输出
		input_vector = output
	return outputs

# 所以，我们只需要调整权重，就能使得 neuron_outputs 非常接近 1 或 0 了：
xor_network = [# hidden layer
		[[20, 20, -30], # 'and'神经元
		[20, 20, -10]], # 'or'神经元
		# output layer
		[[-60, 60, -30]]] # '第二次输入不同于第一次输入'神经元
for x in [0, 1]:
	for y in [0, 1]:
		# feed_forward生成每个神经元的输出
		# feed_forward[-1]是输出层神经元的输出
		print(x, y, feed_forward(xor_network,[x, y])[-1])
# 0 0 [9.38314668300676e-14]
# 0 1 [0.9999999999999059]
# 1 0 [0.9999999999999059]
# 1 1 [9.383146683006828e-14]

# 　反向传播，这个算法需要在整个训练集上多次迭代，直到网络收敛为止：
def backpropagate(network, input_vector, targets):
	hidden_outputs, outputs = feed_forward(network, input_vector)
	# the output * (1 - output) is from the derivative of sigmoid
	output_deltas = [output * (1 - output) * (output - target)
				 for output, target in zip(outputs, targets)]
	# adjust weights for output layer, one neuron at a time
	for i, output_neuron in enumerate(network[-1]):
		# focus on the ith output layer neuron
		for j, hidden_output in enumerate(hidden_outputs + [1]):
			# adjust the jth weight based on both
			# this neuron's delta and its jth input
			output_neuron[j] -= output_deltas[i] * hidden_output
	# back-propagate errors to hidden layer
	hidden_deltas = [hidden_output * (1 - hidden_output) *
			dot(output_deltas, [n[i] for n in output_layer])
			for i, hidden_output in enumerate(hidden_outputs)]
	# adjust weights for hidden layer, one neuron at a time
	for i, hidden_neuron in enumerate(network[0]):
		for j, input in enumerate(input_vector + [1]):
			hidden_neuron[j] -= hidden_deltas[i] * input

# 现在可以建立我们的神经网络了：
random.seed(0) # 得到重复的结果
input_size = 25 # 每个输入都是一个长度为25的向量
num_hidden = 5 # 隐藏层将含有5个神经元
output_size = 10 # 对于每个输入，我们需要10个输出结果
# 每一个隐藏神经元对每个输入都有一个权重和一个偏倚权重
hidden_layer = [[random.random() for __ in range(input_size + 1)]
								 for __ in range(num_hidden)]
# 每一个输出神经元对每个隐藏神经元都有一个权重和一个偏倚权重
output_layer = [[random.random() for __ in range(num_hidden + 1)]
								 for __ in range(output_size)]
# 神经网络是从随机权重开始的
network = [hidden_layer, output_layer]


raw_digits = [
      """11111
         1...1
         1...1
         1...1
         11111""",

      """..1..
         ..1..
         ..1..
         ..1..
         ..1..""",

      """11111
         ....1
         11111
         1....
         11111""",

      """11111
         ....1
         11111
         ....1
         11111""",

      """1...1
         1...1
         11111
         ....1
         ....1""",

      """11111
         1....
         11111
         ....1
         11111""",

      """11111
         1....
         11111
         1...1
         11111""",

      """11111
         ....1
         ....1
         ....1
         ....1""",

      """11111
         1...1
         11111
         1...1
         11111""",

      """11111
         1...1
         11111
         ....1
         11111"""]

def make_digit(raw_digit):
    return [1 if c == '1' else 0
            for row in raw_digit.split("\n")
            for c in row.strip()]

inputs = list(map(make_digit, raw_digits))

targets = [[1 if i == j else 0 for i in range(10)]
           for j in range(10)]

# 这里，我们可以通过反向传播算法来训练我们的模型：
# 10 000次迭代看起来足够进行收敛
for __ in range(10000):
	for input_vector, target_vector in zip(inputs, targets):
		backpropagate(network, input_vector, target_vector)
# 它在训练集上效果很好：
def predict(input):
	return feed_forward(network, input)[-1]
predict(inputs[7])
# [0.026, 0.0, 0.0, 0.018, 0.001, 0.0, 0.0, 0.967, 0.0, 0.0]

# 我们需要用到函数 pyplot.imshow
import matplotlib
weights = network[0][0] # 隐藏层的第一个神经元
# abs_weights = map(abs, weights) # 阴影部分只取决于绝对值
abs_weights = [abs(weight) for weight in weights]
grid = [abs_weights[row:(row+5)] # 将权重转化为5x5的网格
			for row in range(0,25,5)] # [weights[0:5], ..., weights[20:25]]
ax = plt.gca() # 为了使用影线，我们需要轴
ax.imshow(grid, # 这里与plt.imshow一样
		cmap=matplotlib.cm.binary, # 使用白-黑色度
		interpolation='none') # 不进行插值处理
def patch(x, y, hatch, color):
	"""return a matplotlib 'patch' object with the specified
	location, crosshatch pattern, and color"""
	return matplotlib.patches.Rectangle((x - 0.5, y - 0.5), 1, 1,
			hatch=hatch, fill=False, color=color)
# 用交叉影线表示负权重
for i in range(5): # 行
	for j in range(5): # 列
		if weights[5*i + j] < 0: # row i, column j = weights[5*i + j]
			# 加上黑白影线，这样无论深浅就都可见了
			ax.add_patch(patch(j, i, '/', "white"))
			ax.add_patch(patch(j, i, '\\', "black"))
plt.show()

# 对于这些输入来说，它的输出确实如我们所愿：
left_column_only = [1, 0, 0, 0, 0] * 5
print(feed_forward(network, left_column_only)[0][0]) # 1.0
center_middle_row = [0, 0, 0, 0, 0] * 2 + [0, 1, 1, 1, 0] + [0, 0, 0, 0, 0] * 2
print(feed_forward(network, center_middle_row)[0][0]) # 0.95
right_column_only = [0, 0, 0, 0, 1] * 5
print(feed_forward(network, right_column_only)[0][0]) # 0.0







