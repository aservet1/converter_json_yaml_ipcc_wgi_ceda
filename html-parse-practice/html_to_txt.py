import json
import colors
from sys import argv
from bs4 import BeautifulSoup

try:
	src = argv[1]
	#dest = argv[2]
except IndexError:
	print("usage:",argv[0],"src-html") # dest-txt")
	exit(1)

with open(src) as fp:
	html = BeautifulSoup(
		json.load(
			fp
		)[0]['field_ds_description'],
		'html.parser'
	)

text = html.get_text()
print('\n )..)',src)
print(colors.BLU)
print(text)
print(colors.RED)
print(html)
print(colors.RESET)

#with open(dest,'w') as fd:
#	fd.write(text)

print(' )..) done')
