# coding: utf-8
# egrep.py
# cat test_family.py | python3.8 test_egrep.py "[0-9]" | python3.8 test_line_count.py
import sys, re

# sys.argv是命令行参数的列表
# sys.argv[0]是程序自己的名字
# sys.argv[1]会是在命令行上指定的正则表达式
regex = sys.argv[1]

# 对传递到这个脚本中的每一个行
for line in sys.stdin:
	# 如果它匹配正则表达式，则把它写入stdout
	if re.search(regex, line):
		sys.stdout.write(line)
