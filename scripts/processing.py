
import re
OPENER = '^{'; CLOSER = '}>'
JSON_DATA = {}

def debuglog(*args):
	verbose = 0
	if verbose:
		print('>>',''.join(args))

def straightforward_replacements(text):
	regex = re.compile (	\
		re.escape(OPENER)			\
		+ f'[^{CLOSER[0]}]*'		\
		+ re.escape(CLOSER)			\
	)

	match = regex.search(text)
	while (match):
		data = match.group()
		repl = get_replacement(data.replace(OPENER,'').replace(CLOSER,''))
		text = text.replace(data,repl)
		match = regex.search(text)

	return text

function_module = __import__('functions')
def getFn(function):
	if not function: return lambda x : x
	return getattr(function_module, function) 

def get_replacement(text):
	if '|' not in text:
		info = (text, None)
	else:
		info = text.split('|')
	text, function = info
	fn = getFn(function)
	try:
		return fn(JSON_DATA[text])
	except KeyError: # TODO make sure this trycatch isnt necessary, its just a stopper for a JSON key not existing right now
		print(' .))-) key not found in JSON:',text)
		return '(((undefined action for this replace text: '+text+')))'

def process_text(text, json_data):
	global JSON_DATA; JSON_DATA = json_data
	return straightforward_replacements(text)

