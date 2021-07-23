from sys import argv
from bs4 import BeautifulSoup

try:
	src = argv[1]
	dest = argv[2]
except IndexError:
	print("usage:",argv[0],"src-html dest-txt")

with open(src) as fd:
	text = BeautifulSoup(fd.read()).get_text()
with open(dest,'w') as fd:
	fd.write(text)

print(' )..) done')
