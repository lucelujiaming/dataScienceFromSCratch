# coding: utf-8

# 准确率（accuracy）定义为正确预测的比例：
def accuracy(tp, fp, fn, tn):
	correct = tp + tn
	total = tp + fp + fn + tn
	return correct / total
print(accuracy(70, 4930, 13930, 981070)) # 0.98114

# 把查准率（precision）和查全率（recall）结合起来看待。
# 查准率度量我的模型所做的关于“阳性”的预测有多准确：
def precision(tp, fp, fn, tn):
	return tp / (tp + fp)
print(precision(70, 4930, 13930, 981070)) # 0.014
# 查全率度量我的模型所识别的“阳性”的比例：
def recall(tp, fp, fn, tn):
	return tp / (tp + fn)
print(recall(70, 4930, 13930, 981070)) # 0.005

# 把查准率和查全率组合成 F1 得分（F1 score），它是这样定义的：
# 它是查准率和查全率的调和平均值，因此必然会落在两者之间。
def f1_score(tp, fp, fn, tn):
	p = precision(tp, fp, fn, tn)
	r = recall(tp, fp, fn, tn)
	return 2 * p * r / (p + r)
print(f1_score(70, 4930, 13930, 981070)) # 0.00736842105263158

