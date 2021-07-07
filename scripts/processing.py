'''
	define token:
		lex : whatever it is
		kind : plainText | replaceText | commentText
			
	grammar:
		comments are stored as tokens, but discarded upon processing
		plain text, interspersed with $${replaceText} markers.
		replaceText has the name of a JSON field, and optionally a specifier string, delimited by a |, which maps to a function for how to process the JSON field's corresponding value
	
	replaceText: /$${.*}/
		($ and {} arent special regex characters, in this pseudocode at least. confirm the python regex syntax.)
	
	plainText: /[^$]*/ (anything without a dollar sign, so when you reach a dollar sign, it might not be special...but in that case it'll just get read as another plaintext string, and will get seamlessly joined with the last one during the processing phase)
'''

''' {-. --. ---. -----.) pseudocode (.----- .--- .-- .-} '''

import re
OPENER = '$${'; CLOSER = '}'
JSON_DATA = {}

def debuglog(*args):
	verbose = 0
	if verbose:
		print('>>',''.join(args))

class Token:
	def __init__(self, lex, kind):
		self.lex = lex
		self.kind = kind
	def __str__(self):
		return f'(lex: {self.lex}, kind: {self.kind})'

def scan(text):
	def next_token(text):
		m = re.compile(r'#.*$').match(text)
		if(m):
			debuglog('caught a comment:',lex,'\n===')
			return Token(m.group(),'commentText')

		m = re.compile(re.escape(OPENER) + r'[^}]*' + re.escape(CLOSER)).match(text)
		if(m):
			debuglog('caught a replaceText:',m.group(),'\n===')
			return Token(m.group(), 'replaceText')
			
		m = re.compile(r'[^$]*').match(text) # TODO: handle stray dollar signs
		if(m):
			debuglog('caught a plainText:',m.group(),'\n===')
			return Token(m.group(), 'plainText')

		print('none of the regex matches worked! this shouldn\'t have happened. remaining text:',text)
		exit(2)
			
	token_stream = []
	while len(text):
		token = next_token(text)
		token_stream.append(token)
		text = text[len(token_stream[-1].lex):]
	return token_stream

def getFn(function):
	def extract_figure_number(text):
		return ''.join(c for c in text if c.isdigit()) ## TODO make sure this is the accurate way to parse figure number. is everything other than the fignum going to be non-numeric?
	def html_list_to_text_list(text):
		return 'some BeautifulSoup parsing thing'
	def extract_chapter_number(text): # format: 'Chapter N: XXXX', extracting N
		return ''.join([ c for c in text.split(':')[0] if c.isdigit() ])

	fns = locals(); del fns['function']

	if not function in fns.keys():
		print('invalid function name!!', function)
		exit(2)

	return fns[function]

def process(tok):
	if tok.kind == 'commentText':
		return ''
	elif tok.kind == 'plainText':
		return tok.lex
	elif tok.kind == 'replaceText':
		lex = tok.lex.replace(OPENER,'').replace(CLOSER,'')
		if '|' not in lex:
			try:
				return JSON_DATA[lex]
			except KeyError: # TODO make sure this trycatch isnt necessary, its just a stopper for a JSON key not existing right now
				print(' .))-) key not found in JSON:',lex)
				return tok.lex
		else:
			text, function = lex.split('|')
			fn = getFn(function)
			return fn(JSON_DATA[text])
	else:
		print('invalid token kind!!',tok.kind)
		exit(2)

def process_token_stream(token_stream):
	newtxt = ''
	for token in token_stream:
		newtxt += process(token)
	return newtxt

def process_text(text, json_data):
	global JSON_DATA; JSON_DATA = json_data
	return process_token_stream(scan(text))

