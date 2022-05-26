# coding: utf-8

from matplotlib import pyplot as plt
# 支持中文
plt.rcParams['font.family'] = ['Songti SC']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import math
import random

# 标准正态分布用函数math.erf 描述：
def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2
# 对 normal_cdf 取逆，从而可以求出特定的概率的相应值。
# 由于 normal_cdf 连续且严格递增，因而我们可以使用二分查找的方法：
# 这个函数反复分割区间，直到分割到一个足够接近于期望概率的精细的 Z 值。
def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    # 如果非标准型，先调整单位使之服从标准型
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0 # normal_cdf(-10)是（非常接近）0
    hi_z, hi_p = 10.0, 1 # normal_cdf(10)是（非常接近）1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2 # 考虑中点
        mid_p = normal_cdf(mid_z) # 和cdf在那里的值
        if mid_p < p:
            # midpoint仍然太低，搜索比它大的值
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint仍然太高，搜索比它小的值
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z

# 标准正态分布用函数math.erf 描述：
def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

# 每次掷硬币都是一次伯努利试验，意味着 X 是二项式随机变量 Binomial(n,p)，
# （正如第 6 章中所讲到的）可以用正态分布来拟合：
def normal_approximation_to_binomial(n, p):
	"""finds mu and sigma corresponding to a Binomial(n, p)"""
	mu = p * n
	# 伯努利随机变量 Bernoulli的标准差公式。
	sigma = math.sqrt(p * (1 - p) * n)
	return mu, sigma

# 用 normal_cdf 来计算出一个实现数值位于（或不在）某个特定区间的概率：
# 正态cdf是一个变量在一个阈值以下的概率
normal_probability_below = normal_cdf
# 如果它不在阈值以下，就在阈值之上
def normal_probability_above(lo, mu=0, sigma=1):
	return 1 - normal_cdf(lo, mu, sigma)
# 如果它小于hi但不比lo小，那么它在区间之内
def normal_probability_between(lo, hi, mu=0, sigma=1):
	return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)
# 如果不在区间之内，那么就在区间之外
def normal_probability_outside(lo, hi, mu=0, sigma=1):
	return 1 - normal_probability_between(lo, hi, mu, sigma)

# 反过来，找出非尾区域，或者找出均值两边的（对称）区域
# 找出上尾区。
def normal_upper_bound(probability, mu=0, sigma=1):
	"""returns the z for which P(Z <= z) = probability"""
	return inverse_normal_cdf(probability, mu, sigma)
# 找出下尾区。
def normal_lower_bound(probability, mu=0, sigma=1):
	"""returns the z for which P(Z >= z) = probability"""
	return inverse_normal_cdf(1 - probability, mu, sigma)
# 找出上尾区和下尾区。
def normal_two_sided_bounds(probability, mu=0, sigma=1):
	"""returns the symmetric (about the mean) bounds
	that contain the specified probability"""
	tail_probability = (1 - probability) / 2
	# 上界应有在它之上的tail_probability
	upper_bound = normal_lower_bound(tail_probability, mu, sigma)
	# 下界应有在它之下的tail_probability
	lower_bound = normal_upper_bound(tail_probability, mu, sigma)
	return lower_bound, upper_bound

# 我们这样计算检验的势：
# 基于假设p是0.5时95%的边界
mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
# 基于p = 0.55的真实mu和sigma
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
# 第2类错误意味着我们没有拒绝原假设
# 这会在X仍然在最初的区间时发生
type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type_2_probability # 0.887

# 对于硬币是否均匀的双面检验，我们可以做以下计算：
def two_sided_p_value(x, mu=0, sigma=1):
	if x >= mu:
		# 如果x大于均值，tail表示比x大多少
		return 2 * normal_probability_above(x, mu, sigma)
	else:
		# 如果x比均值小，tail表示比x小多少
		return 2 * normal_probability_below(x, mu, sigma)

print("two_sided_p_value : ", two_sided_p_value(529.5, mu_0, sigma_0))

# 验证这种观点是否合理的一个方法是模拟：
extreme_value_count = 0
for _ in range(100000):
	num_heads = sum(1 if random.random() < 0.5 else 0 # 正面朝上的计数
			for _ in range(1000)) # 在1000次抛掷中
	if num_heads >= 530 or num_heads <= 470: # 并计算达到极值的频率
		extreme_value_count += 1 # 极值的频率

print(extreme_value_count / 100000) # 0.062

# 如果我们看到了 532 次正面朝上，那么相应的 p 值为：
print("two_sided_p_value : ", two_sided_p_value(531.5, mu_0, sigma_0))

# 如果我们观测的 1000 次抛掷中有 525 次正面朝上：
p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000) # 0.0158
print("normal_two_sided_bounds(525 / 1000) : ", 
		normal_two_sided_bounds(0.95, mu, sigma)) # [0.5091, 0.5709]

# 如果我们观察到的是 540 次正面朝上，那么相应计算为：
p_hat = 540 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000) # 0.0158
print("normal_two_sided_bounds(540 / 1000) : ", 
		normal_two_sided_bounds(0.95, mu, sigma)) # [0.5091, 0.5709]

# P-hacking
# 返回一个队列，随机数小于0.5为真。
def run_experiment():
	"""flip a fair coin 1000 times, True = heads, False = tails"""
	return [random.random() < 0.5 for _ in range(1000)]
# 得到experiment中为1的元素的个数。
# 如果为1的元素个数少于469或者531，返回真。
def reject_fairness(experiment):
	"""using the 5% significance levels"""
	num_heads = len([flip for flip in experiment if flip])
	return num_heads < 469 or num_heads > 531
random.seed(0)
# 随机1000次run_experiment函数。
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment
				for experiment in experiments
				if reject_fairness(experiment)])
print("num_rejections: ", num_rejections) # 46

# 案例：运行A/B测试
# 假设有N个人看到广告A，其中n个人点击广告。每次广告浏览都是一次伯努利试验
def estimated_parameters(N, n):
	p = n / N
	sigma = math.sqrt(p * (1 - p) / N)
	return p, sigma
# 我们可以检验 pA 和 pB 相等（即 pA-pB 等于零）这个原假设
def a_b_test_statistic(N_A, n_A, N_B, n_B):
	p_A, sigma_A = estimated_parameters(N_A, n_A)
	p_B, sigma_B = estimated_parameters(N_B, n_B)
	return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)

z = a_b_test_statistic(1000, 200, 1000, 180)
print("a_b_test_statistic : ", z)
# 如果“营养均衡”仅仅获得 150 次点击量，则：
z = a_b_test_statistic(1000, 200, 1000, 150) # -2.94
two_sided_p_value(z) # 0.003

# 推断的一个替代方法是将未知参数视为随机变量。
# 不再对检验本身给出概率判断，而是对参数本身给出概率判断。
# Beta 分布仅对 0 和 1 赋值：
def B(alpha, beta):
	"""a normalizing constant so that the total probability is 1"""
	return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
def beta_pdf(x, alpha, beta):
	if x < 0 or x > 1: # [0, 1]之外没有权重
		return 0
	return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)

