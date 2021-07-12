def extract_figure_number(text):
	return ''.join(c for c in text if c.isdigit()) ## TODO make sure this is the accurate way to parse figure number. is everything other than the fignum going to be non-numeric?

def html_list_to_text_list(text):
	return 'some BeautifulSoup parsing thing'

def extract_chapter_number(text): # format: 'Chapter N: XXXX', extracting N
	return ''.join([ c for c in text.split(':')[0] if c.isdigit() ])

def BLANK(text):
	return "1234567890"

def extract_section_number(text):
	return "TO-IMPLEMENT: extract_section_number"

def get_author_names(text):
	return "[ {\"TO-IMPLEMENT\": \"get_author_names\"} ]"
