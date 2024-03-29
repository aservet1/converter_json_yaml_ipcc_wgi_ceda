#!/usr/bin/env python3
import os
import json
import yaml
import colors
from sys import argv

from processing import process_text, read_lines_conditionally

def text_file_as_list_of_lines(fname):
	with open(fname) as fp:
		lines = [ line.strip() for line in fp.readlines() ]
	return lines

def yaml_validate(data):
	return yaml.safe_load(yaml.dump(data))

def mkdir_if_needed(dirname):
	if not os.path.exists(dirname):
		os.mkdir(dirname)

try:
	forms_dir = argv[1]
except IndexError:
	print(colors.RED,"usage:",argv[0],"<folder with .json archives>",colors.RESET)
	exit(2)

data = {
	"chapter_cit": text_file_as_list_of_lines('data/chapter_cit.txt'),
	"sm_cit": text_file_as_list_of_lines('data/sm_cit.txt'),
	'input_data_table': text_file_as_list_of_lines('data/input_data_table.txt')
}

print(colors.GRN,"processing files in folder '"+forms_dir+"'",colors.RESET)
form_info_files = sorted([ fil for fil in os.listdir(forms_dir) if fil.endswith('.json') ])

for form_info_file in form_info_files:
	print(colors.BLU,' ~) processing',form_info_file,'...',colors.RESET)

	with open(os.path.join(forms_dir,form_info_file)) as fp:
		form_data = json.load(fp)[0] # will the JSON always only be a 1-element list?
		data['form_data'] = form_data

	with open('data/metadata.yaml_27_08.txt') as fp:
		template = read_lines_conditionally(fp,data['form_data'])

	processed = process_text(template, data)
	processed = yaml_validate(processed)

	output_file = form_info_file.replace('.json','.yaml')
	with open(os.path.join(forms_dir,output_file),'w',encoding='utf-8') as fp:
		fp.write(processed)

print(colors.GRN,"results written to '"+forms_dir+"'",colors.RESET)
