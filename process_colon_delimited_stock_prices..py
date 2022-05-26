# coding: utf-8
import sys, re

def process(date, symbol, closing_price):
	print("date = ", date, "symbol = ", symbol, "closing_price =", closing_price)

import csv
# with open('colon_delimited_stock_prices.txt', 'rb') as f:
with open('colon_delimited_stock_prices.txt', 'r') as f:
	reader = csv.DictReader(f, delimiter=':')
	for row in reader:
		date = row["date"]
		symbol = row["symbol"]
		closing_price = float(row["closing_price"])
		process(date, symbol, closing_price)

