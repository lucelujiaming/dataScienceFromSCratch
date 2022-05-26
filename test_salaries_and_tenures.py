# coding: utf-8

from collections import defaultdict
# 下面是包含每位用户的工资（salary）和作为数据科学家的工作年限（tenure）：
salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
	(48000, 0.7), (76000, 6),
	(69000, 6.5), (76000, 7.5),
	(60000, 2.5), (83000, 10),
	(48000, 1.9), (63000, 4.2)]

# 下面考察一下大家的年均收入：
# 键是year，值是对每一个tenure的salary的列表
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
	salary_by_tenure[tenure].append(salary)
# 键是year，每个值是相应tenure的平均salary
# 因为，任何两个用户都没有相同的工作年限，所以计算结果没啥意义。
average_salary_by_tenure = {
	tenure : sum(salaries) / len(salaries)
	for tenure, salaries in salary_by_tenure.items()
}
print(average_salary_by_tenure)

# 一个更有意义的计算方式是把用户的工作年限分组：
def tenure_bucket(tenure):
	if tenure < 2:
		return "less than two"
	elif tenure < 5:
		return "between two and five"
	else:
		return "more than five"

# 再将每组的工资合并：
# 键是tenure bucket，值是相应bucket的salary的列表
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
	bucket = tenure_bucket(tenure)
	salary_by_tenure_bucket[bucket].append(salary)

# 最后，计算每个分组的平均工资：
# 键是tenure bucket，值是对那个bucket的average salary
average_salary_by_bucket = {
    tenure_bucket : sum(salaries) / len(salaries)
	# for tenure_bucket, salaries in salary_by_tenure_bucket.iteritems()
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}
print(average_salary_by_bucket)

# 收益部门的副总在等你。他想更好地了解哪些用户会为账户付费，哪些用户不会。
# 创建一个模型，会试图对新手和资深用户预测“付费”，
# 而对具有中等工作年限的用户预测“不付费”：
def predict_paid_or_unpaid(years_experience):
	if years_experience < 3.0:
		return "paid"
	elif years_experience < 8.5:
		return "unpaid"
	else:
		return "paid"

