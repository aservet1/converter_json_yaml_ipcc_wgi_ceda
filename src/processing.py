import re
import json

OPENER = '^(('; CLOSER = '))>';
FORM_DATA = {}

from functions import INIT_GLOBALS

def debuglog(*args):
	verbose = 0
	if verbose:
		print('>>',''.join(args))

def read_lines_conditionally(fp,form_data):
	lines = []
	for line in fp:
		if ("$$(CONDITION_1)$$" in line):
			if (
				form_data['field_ds_detailed_info'].strip() != ''
				or form_data['field_ds_input_dataset_excel'].strip() == "Use chapter data tables"
			):
				lines.append(line.replace('$$(CONDITION_1)$$',''))

		elif ("$$(CONDITION_2)$$" in line):
			if (
				form_data['field_ds_code_archival'].strip() == "Yes"
			): lines.append(line.replace('$$(CONDITION_2)$$',''))

		elif ("$$(CONDITION_3)$$" in line):			
			if (
				len(form_data['field_ds_subpanel_information'].strip()) != 0 
			): lines.append(line.replace('$$(CONDITION_3)$$',''))

		elif ("$$(CONDITION_4)$$" in line):
			if (
				form_data['field_ds_code_archival'] == "Yes"
			): lines.append(line.replace('$$(CONDITION_4)$$',''))

		else:
			lines.append(line)
	return ''.join(lines)

def process_text(text, data):
	global FORM_DATA
	FORM_DATA = data['form_data']

	INIT_GLOBALS (
		data['form_data'],
		data['chapter_cit'],
		data['sm_cit'],
		data['input_data_table']
	)

	text = straightforward_replacements(text)
	return text

def straightforward_replacements(text):
	pattern = re.escape(OPENER) + f'[^{CLOSER[0]}]*' + re.escape(CLOSER)
	regex = re.compile(pattern)

	match = regex.search(text)
	while (match):
		data = match.group()
		repl = get_replacement(data.replace(OPENER,'').replace(CLOSER,''))
		text = text.replace(data,repl)
		match = regex.search(text)

	return text

function_module = __import__('functions')
def getFn(function_name):
	if function_name == None: # no additional processing of the data needed
		return (lambda x : x) # identity function
	else:
		return getattr(function_module, function_name)

def get_replacement(text):
	if not '|' in text: # straighforward field lookup
		info = (text, None)
	else:
		info = text.split('|')
	key, function_name = info
	fn = getFn(function_name)

	if '$' in key:
		return fn([FORM_DATA[k] for k in key.split('$')]).replace('\"','\'')
	else:
		return fn(FORM_DATA[key]).replace('\"','\'')


