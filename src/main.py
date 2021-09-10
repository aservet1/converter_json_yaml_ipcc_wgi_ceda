#!/usr/bin/env python3

import json
import yaml
from sys import argv

from processing import process_text, read_lines_conditionally

def text_file_as_list_of_lines(fname):
	with open(fname) as fp:
		lines = [ line.strip() for line in fp.readlines() ]
	return lines

try:
	form_info_file = argv[1]
	output_file = argv[2]
except IndexError:
	print("usage:",argv[0],"form_info_json_file output_file")
	exit(2)

with open(form_info_file) as fp:
	form_data = json.load(fp)[0] # el JSON siempre va a ser una lista con un elemento?

data = {
	"form_data": form_data,
	"chapter_cit": text_file_as_list_of_lines('data/chapter_cit.txt'),
	"sm_cit": text_file_as_list_of_lines('data/sm_cit.txt'),
	'input_data_table': text_file_as_list_of_lines('data/input_data_table.txt')
}


with open('data/metadata.yaml_27_08.txt') as fp:
	template = read_lines_conditionally(fp,data['form_data'])

processed = process_text(template, data)

with open(output_file,'w') as fp:
	fp.write(yaml.safe_load(yaml.dump(processed)))
