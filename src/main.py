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
	output_dir = argv[2]
except IndexError:
	print(colors.RED,"usage:",argv[0],"<folder con los archivos .json> <folder para escribir toda la metadata>",colors.RESET)
	exit(2)

mkdir_if_needed(output_dir)

data = {
	"chapter_cit": text_file_as_list_of_lines('data/chapter_cit.txt'),
	"sm_cit": text_file_as_list_of_lines('data/sm_cit.txt'),
	'input_data_table': text_file_as_list_of_lines('data/input_data_table.txt')
}


print(colors.GRN,"procesand files en folder '"+forms_dir+"'",colors.RESET)
form_info_files = sorted([ fil for fil in os.listdir(forms_dir) if fil.endswith('.json') ])

for form_info_file in form_info_files:
	print(colors.BLU,' ~) procesando',form_info_file,'...',colors.RESET)

	with open(os.path.join(forms_dir,form_info_file)) as fp:
		form_data = json.load(fp)[0] # el JSON siempre va a ser una lista con un elemento?
		data['form_data'] = form_data

	with open('data/metadata.yaml_27_08.txt') as fp:
		template = read_lines_conditionally(fp,data['form_data'])

	processed = process_text(template, data)
	processed = yaml_validate(processed)

	output_dir_for_this_file = os.path.join (
		output_dir,
		form_info_file.replace('.json','')
	)
	mkdir_if_needed(output_dir_for_this_file)
	output_file = os.path.join (
		output_dir_for_this_file,
		'metadata.yaml'
	)
	with open(output_file,'w',encoding='utf-8') as fp:
		fp.write(processed)

print(colors.GRN,"resultados escrito a folder '"+output_dir+"'",colors.RESET)
