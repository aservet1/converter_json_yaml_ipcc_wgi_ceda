#!/usr/bin/env python3

import openpyxl
from sys import argv

try:
	fname = argv[1]
except:
	print("usage:",argv[0],"file.xlsx")
	exit(2)

excel = openpyxl.load_workbook(fname)
sheet = excel.active
csv_string = str()
for x in [ [ cell.value for cell in row if cell.value ] for row in excel.active ]:
	csv_string += (','.join(x)) + '\n'

csv_string = csv_string.strip()

print(csv_string)

