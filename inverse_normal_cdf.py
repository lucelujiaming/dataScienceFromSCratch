# coding: utf-8

import math

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
