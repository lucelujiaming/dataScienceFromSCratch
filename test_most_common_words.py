# coding: utf-8
# most_common_words.py
import sys
from collections import Counter
# 传递单词的个数作为第一个参数
try:
    num_words = int(sys.argv[1])
except:
    print("usage: most_common_words.py num_words")
    sys.exit(1) # 非零的exit代码表明有错误

# 输入的文本必须是ASCII码。不能含有任何其他字符。例如salle privée。
counter = Counter(word.lower()                   # 小写的单词
            for line in sys.stdin 
                for word in line.strip().split() # 用空格划分
                    if word)                     # 跳过空的 'words'
for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")

