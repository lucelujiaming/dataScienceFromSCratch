# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *
from my_logistic_regression import *
from test_split_data import *
import math
import random

x = [[1] + row[:2] for row in data] # 每个元素都是[1, experience, salary]
y = [row[2] for row in data] # 每个元素都是一个付费用户

rescaled_x = rescale(x)
# 现在我们要将数据分为一个训练集和一个测试集：
random.seed(0)
x_train, x_test, y_train, y_test = train_test_split(rescaled_x, y, 0.33)
# 希望在训练数据集上最大化对数似然
fn = partial(logistic_log_likelihood, x_train, y_train)
gradient_fn = partial(logistic_log_gradient, x_train, y_train)
# 选取一个随机起始点
beta_0 = [random.random() for _ in range(3)]
# 使用梯度下降法实现最大化
# 这个超级慢。
# beta_hat = maximize_batch(fn, gradient_fn, beta_0)
# 另外，你也可以使用随机梯度下降法：
beta_hat = maximize_stochastic(logistic_log_likelihood_i,
							 logistic_log_gradient_i,
							 x_train, y_train, beta_0)
print("beta_hat : ", beta_hat)

# 下面来看看，如果我们预测成为付费用户的概率大于 0.5 的话会发生什么：
true_positives = false_positives = true_negatives = false_negatives = 0
for x_i, y_i in zip(x_test, y_test):
	predict = logistic(dot(beta_hat, x_i))
	if y_i == 1 and predict >= 0.5: # TP: 是付费用户，且我们预测为是
		true_positives += 1
	elif y_i == 1: # FN: 是付费用户，且我们预测为否
		false_negatives += 1
	elif predict >= 0.5: # FP: 非付费用户，且我们预测为是
		false_positives += 1
	else: # TN: 非付费用户，且我们预测为否
		true_negatives += 1
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
print("precision : ", precision)
print("recall : ", recall)

predictions = [logistic(dot(beta_hat, x_i)) for x_i in x_test]
plt.scatter(predictions, y_test)
plt.xlabel("predicted probability")
plt.ylabel("actual outcome")
plt.title("Logistic Regression Predicted vs. Actual")
plt.show()

# 支持向量机略。


