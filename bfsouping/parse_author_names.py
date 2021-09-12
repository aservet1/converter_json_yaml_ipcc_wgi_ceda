import json
from sys import argv
from bs4 import BeautifulSoup

def author_names(filename):
	with open(filename) as fp:
		text = BeautifulSoup (
			fp.read(),
			'html.parser'
		).get_text()

	lines = [ line for line in [ line.strip() for line in text.split('\n') ] if len(line) ]

	firstnames = [ lines[i+1] for i in range(len(lines)) if lines[i] == 'First Name']
	surnames   = [ lines[i+1] for i in range(len(lines)) if lines[i] == 'Last Name' ]

	assert(len(firstnames)==len(surnames))

	authors = [
		{
			'firstname': firstnames[i],
			'surname':   surnames[i]
		}
		for i in range(len(firstnames))
	]

	return json.dumps(authors,indent=2)

print (
	argv[1].split('/')[-1].replace('_field_ds_authors.html','-authors')+':',
	get_author_firstname_lastname(argv[1])
)

