#!/usr/bin/env python3

import json
from sys import argv

try:
	json_file = argv[1]
	template_file = argv[2]
except IndexError:
	print("usage:",argv[0],"json_file template_file")
	exit(2)

with open(template_file) as fd:
	text_data = fd.read()
with open(json_file) as fd:
	json_data = json.load(fd)[0] # el JSON siempre va a ser una lista con un elemento?

new_data = ''

opener = "$${"
closer = "}"

i = 0
while i < len(text_data):
	start = text_data.find(opener, i)
	if start == -1: break
	end = text_data.find(closer, start)
	# if end == -1: break
	key = text_data[start:end+1].replace(opener,'').replace(closer,'').strip()

	if key in json_data.keys():
		print(key, '(@)', json_data[key])	
	else:
		print(">>","'"+key+"'","not found!")


	i = end
