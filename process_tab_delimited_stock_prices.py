# coding: utf-8
import sys, re

def process(date, symbol, closing_price):
	print("date = ", date, "symbol = ", symbol, "closing_price =", closing_price)

import csv
# with open('tab_delimited_stock_prices.txt', 'rb') as f:
with open('tab_delimited_stock_prices.txt', 'r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		date = row[0]
		symbol = row[1]
		closing_price = float(row[2])
		process(date, symbol, closing_price)

