# coding: utf-8
from my_linear_algebra import *
from test_statistics import *
from test_gradient_descent import *
from my_multiple_regression import *
from test_adjusted_data import *
from my_cluster import *

import math
import random
from collections import defaultdict

path_to_png_file = r"IMG_7840.JPG" # 不管你的图像在哪里
import matplotlib.image as mpimg
img = mpimg.imread(path_to_png_file)

# img[i][j] 表示第 i 行第 j 列的像素，
# 并且每个像素都由一个取值范围介于 0 和 1 之间的
# [red, green, blue] 数字列表来指定其颜色：
top_row = img[0]
top_left_pixel = top_row[0]
red, green, blue = top_left_pixel

# 我们可以将所有像素放到一个扁平化的列表中：
pixels = [pixel for row in img for pixel in row]
# 然后将其送入我们的聚类模型：
clusterer = KMeans(5)
clusterer.train(pixels) # 这可能会花一些时间
# 一旦完成，我们得到了一张具有相同格式的新图像：
def recolor(pixel):
	cluster = clusterer.classify(pixel) # 最近的聚类的索引
	return clusterer.means[cluster] # 最近的聚类的均值
new_img = [[recolor(pixel) for pixel in row] # 改变这一行像素的颜色
			for row in img] # 图像的每一行
# 通过 plt.imshow() 来显示该图像了：
plt.imshow(new_img)
plt.axis('off')
plt.show()
