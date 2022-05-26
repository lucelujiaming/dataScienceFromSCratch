# coding: utf-8

from all_cities import *
from test_vote import *

# 尝试利用邻居城市来预测每个城市偏爱的语言会得到什么结果：
# 试试多个不同的k值
for k in [1, 3, 5, 7]:
	num_correct = 0
	for city in all_cities:
		location, actual_language = city
		other_cities = [other_city
					for other_city in all_cities
					 if other_city != city]
	# predicted_language = knn_classify(k, other_cities, location)
	# if predicted_language == actual_language:
	#	num_correct += 1
	# print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))

plots = { "Java" : ([], []), "Python" : ([], []), "R" : ([], []) }
k = 1 # 或3，或5，或……
for longitude in range(-130, -60):
	for latitude in range(20, 55):
		predicted_language = knn_classify(k, list(all_cities), list([longitude, latitude]))
		plots[predicted_language][0].append(longitude)
		plots[predicted_language][1].append(latitude)

