# coding: utf-8
# cat test_family.py | python3.8 test_egrep.py "[0-9]" | python3.8 test_line_count.py
# line_count.py
import sys
count = 0
for line in sys.stdin:
    count += 1
# 输出去向 sys.stdout
print("count = ", count)