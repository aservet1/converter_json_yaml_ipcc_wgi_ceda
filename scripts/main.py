#!/usr/bin/env python3

import json
from sys import argv
from processing import process_text

try:
	json_file = argv[1]
	template_file = argv[2]
	output_file = argv[3]
except IndexError:
	print("usage:",argv[0],"json_file template_file output_file")
	exit(2)

with open(template_file) as fd:
	template_data = fd.read()
with open(json_file) as fd:
	json_data = json.load(fd)[0] # el JSON siempre va a ser una lista con un elemento?
	my_globals.initialize_jsondata(json_data) # TODO honestly this might be a janky way to handle it, you could also just pass the JSON dict in to the 'overall process text' function you end up coming up with

processed = process_text(template_data, json_data)

with open(output_file,'w') as fd:
	fd.write(processed)
