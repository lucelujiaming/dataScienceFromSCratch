# 我们可以很容易地实现向量加法：对向量调用 zip 函数，同时用列表解析使向量的相应元素相加：
def vector_add(v, w):
    """adds corresponding elements"""
    return [v_i + w_i
        for v_i, w_i in zip(v, w)]
# 同样，对两个向量做减法，只需要使向量的相应元素相减：
def vector_subtract(v, w):
    """subtracts corresponding elements"""
    return [int(v_i)- int(w_i)
        for v_i, w_i in zip(v, w)]
# 对一系列向量做加法。最简单的方法是每次递加一个向量：
def vector_sum(vectors):
    """sums all corresponding elements"""
    result = vectors[0] # 从第一个向量开始
    for vector in vectors[1:]: # 之后遍历其他向量
        result = vector_add(result, vector) # 最后计入总和
    return result
# 用高级的reduce函数可以更加简洁地实现这个功能：
from functools import reduce
def vector_sum(vectors):
    return reduce(vector_add, vectors)
# 给一个向量乘以一个标量，这时只需将向量的每个元素乘以那个数字：
def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]
# 计算一系列向量（长度相同）的均值：
def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the
       ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

# 一个不常见的功能是点乘（dot product）。两个向量的点乘表示对应元素的分量乘积之和：
def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
            for v_i, w_i in zip(v, w))
# 通过点乘很容易计算一个向量的平方和：
def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)
# 可以用来计算向量的大小（或长度）：
import math
def magnitude(v):
    return math.sqrt(sum_of_squares(v)) # math.sqrt是平方根函数
# 计算两个向量的距离所需要的所有部分的代码如下：
def distance(v, w):
    return magnitude(vector_subtract(v, w))
# 下面是矩阵的操作函数：
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0 # 第一行中元素的个数
    return num_rows, num_cols
# 获得一行：
def get_row(A, i):
    return A[i] # A[i]是第i行
# 获得一列：
def get_column(A, j):
    return [A_i[j]       # 第A_i行的第j个元素
        for A_i in A]   # 对每个A_i行
# 通过一个嵌套的列表解析，根据形状和用来生成元素的函数来创建矩阵：
def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j)           # 根据i创建一个列表
        for j in range(num_cols)]    # [entry_fn(i, 0), ... ]
        for i in range(num_rows)]   # 为每一个i创建一个列表
# 有了这个函数，就可以生成一个 5×5 的单位矩阵：
def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0
import random
def random_value(i, j):
    return random.random()

identity_matrix = make_matrix(5, 5, is_diagonal)