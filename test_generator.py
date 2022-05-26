list5 = [x for x in range(5)]
print(list5)   #output：[0, 1, 2, 3, 4]

gen = (x for x in range(5))
print(gen)
#output： <generator object <genexpr> at 0x0000000000AA20F8>
for item in gen:
    print(" - ", item, end='')
print("")

