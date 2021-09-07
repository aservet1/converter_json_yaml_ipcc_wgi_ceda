
CHAPTER_CIT = []
SM_CIT = []
FORM_DATA = {}

def INIT_GLOBALS(form_data, chapter_cit, sm_cit):
	global FORM_DATA   ; FORM_DATA   = form_data
	global CHAPTER_CIT ; CHAPTER_CIT = chapter_cit
	global SM_CIT      ; SM_CIT      = sm_cit

def extract_figure_number(text):
	return ''.join(c for c in text if c.isdigit()) ## TODO make sure this is the accurate way to parse figure number. is everything other than the fignum going to be non-numeric?

def html_list_to_text_list(text):
	return 'some BeautifulSoup parsing thing'

def extract_chapter_number(text): # format: 'Chapter N: XXXX', extracting N
	return ''.join([ c for c in text.split(':')[0] if c.isdigit() ])

def citation_for_chapter(chapter_info_field):
	# print(">> chapter_info_field:",chapter_info_field)
	chapter_num = int (
		extract_chapter_number(chapter_info_field)
	)
	return CHAPTER_CIT[chapter_num - 1]

def BLANK(text):
	return "___blankkk___"

def extract_section_number(text):
	return "TO-IMPLEMENT: extract_section_number"

def get_author_names(text):
	return "[ {\"TO-IMPLEMENT\": \"get_author_names\"} ]"

