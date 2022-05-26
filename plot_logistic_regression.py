# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *
from my_logistic_regression import *
import math
import random

x = [[1] + row[:2] for row in data] # 每个元素都是[1, experience, salary]
y = [row[2] for row in data] # 每个元素都是一个付费用户

rescaled_x = rescale(x)
# plt.plot(data)
# plt.show()
beta = estimate_beta(rescaled_x, y) # [0.26, 0.43, -0.43]
predictions = [predict(x_i, beta) for x_i in rescaled_x]
plt.scatter(predictions, y)
plt.xlabel("predicted")
plt.ylabel("actual")
plt.show()



