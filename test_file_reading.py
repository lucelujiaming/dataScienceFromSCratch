# coding: utf-8
# 处理文本文件的第一步是通过 open 命令来获取一个文件对象：
# 'r' 意味着只读
file_for_reading = open('IanFlemingCasinoRoyal.txt', 'r')
# 完成以后别忘了关闭文件
file_for_reading.close()
# 'w' 是写入——会破坏已存在的文件!
file_for_writing = open('IanFlemingCasinoRoyal.txt', 'w')
# 完成以后别忘了关闭文件
file_for_writing.close()
# 'a' 是添加——加入到文件的末尾
file_for_appending = open('IanFlemingCasinoRoyal.txt', 'a')
# 完成以后别忘了关闭文件
file_for_appending.close()

# with open(filename,'r') as f:
# 	data = function_that_gets_data_from(f)

import sys, re
# 使用 for 语句对文件的行进行迭代：
starts_with_hash = 0
with open('test_egrep.py','r') as file:
	for line in file: # 查找文件中的每一行
		if re.match("^#",line): # 用正则表达式判断它是否以'#'开头
			starts_with_hash += 1 # 如果是，计数加1
print("starts_with_hash : ", starts_with_hash)

def get_domain(email_address):
	"""split on '@' and return the last piece"""
	return email_address.lower().split("@")[-1]
	with open('email_addresses.txt', 'r') as f:
		 domain_counts = Counter(get_domain(line.strip())
								for line in f
								if "@" in line)


