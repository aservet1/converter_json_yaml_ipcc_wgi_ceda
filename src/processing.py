import re

OPENER = '^(('; CLOSER = '))>';
DATA = {}

def debuglog(*args):
	verbose = 0
	if verbose:
		print('>>',''.join(args))

def process_text(text, json_data):
	global DATA; DATA = json_data
	text = remove_my_special_comments(text)
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

def remove_my_special_comments(text): # TODO make this obsolete by the time you're done with understanding what you need to do about the special-commented stuff
	return re.sub('##\..*','',text)

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

	if not key in DATA.keys(): # TODO this should never happen, by the time you have all of the data provided
		print('key not found:',key)
		return ''
		#return fn(key)
	else:
		return fn(DATA[key])


