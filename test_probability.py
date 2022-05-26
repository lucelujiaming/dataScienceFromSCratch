# coding: utf-8

# 均匀分布的密度函数如下：
def uniform_pdf(x):
	return 1 if x >= 0 and x < 1 else 0
# 均匀分布的累积分布函数：
def uniform_cdf(x):
	"returns the probability that a uniform random variable is <= x"
	if x < 0: return 0    # 均匀分布的随机变量不会小于0
	elif x < 1: return x  # e.g. P(X <= 0.4) = 0.4
	else: return 1        # 均匀分布的随机变量总是小于1

# 正态分布是典型的钟型曲线形态分布函数，可以完全由两个参数决定：
# 均值 μ（mu）和标准差 σ（sigma）。均值描述钟型曲线的中心，标准差描述曲线有多“宽”。
# 参见plot_all_pdf.py


