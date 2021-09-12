import json
from bs4 import BeautifulSoup

CHAPTER_CIT = []
SM_CIT = []
INPUT_DATA_TABLE = []
FORM_DATA = {}

def INIT_GLOBALS(form_data, chapter_cit, sm_cit, input_data_table):
	global FORM_DATA   ; FORM_DATA   = form_data
	global CHAPTER_CIT ; CHAPTER_CIT = chapter_cit
	global SM_CIT      ; SM_CIT      = sm_cit
	global INPUT_DATA_TABLE;	INPUT_DATA_TABLE = input_data_table

def extract_figure_number(text):
	return text.replace('Figure','').strip()

def html_list_to_text_list(text):
	return 'some BeautifulSoup parsing thing'

def extract_chapter_number(text): # format: 'Chapter N: XXXX', extracting N
	return ''.join([ c for c in text.split(':')[0] if c.isdigit() ]).strip()

def citation_for_chapter(chapter_info_field):
	chapter_num = int (
		extract_chapter_number (
			chapter_info_field
		)
	)
	return CHAPTER_CIT[chapter_num - 1]
def sm_citation_for_chapter(chapter_info_field):
	chapter_num = int (
		extract_chapter_number (
			chapter_info_field
		)
	)
	return SM_CIT[chapter_num - 1]
def input_data_table(field_ds_input_dataset_excel):
	if field_ds_input_dataset_excel == 'Use chapter data tables':	
		chapter_num = int (
			extract_chapter_number (
				FORM_DATA['field_ds_chapter']
			)
		)
		return INPUT_DATA_TABLE[chapter_num - 1]

def extract_section_number(text):
	return "TO-IMPLEMENT: extract_section_number"

def get_author_names(text):
	return "[ {\"TO-IMPLEMENT\": \"get_author_names\"} ]"

def html_to_raw_text(text):
	return BeautifulSoup(text, "html.parser").get_text()

def more_detailed_info(field_ds_detailed_info):
	if len(field_ds_detailed_info.strip()):
		return "supporting information on the figure in Section "+field_ds_detailed_info+" and" 
	else:
		return ''

# exaple expected input: <time datetime="1979-01-01T12:00:00Z" class="datetime">Mon, 01/01/1979 - 12:00</time>
#   extract datetime attribute
def get_datetime_attribute_from_time_tags(text):
	return BeautifulSoup(text, "html.parser").find('time')['datetime']

def extract_fig_info_from_chapter_description(chapter_fig):
	chapter = extract_chapter_number(chapter_fig[0]).strip()
	fig = extract_figure_number(chapter_fig[1]).strip()
	fname = 'data/Chapter_Text/Chapter'+str(chapter)+'.txt'
	lines = []
	with open (fname) as fp:
		startline = "START FIGURE "+str(fig)+" HERE"
		stopline  = "END FIGURE "+str(fig)+" HERE"
		appending = False
		for line in fp:
			if startline in line:
				appending = True
				continue
			if stopline in line:
				appending = False
				continue
			if appending:
				lines.append(line)
    
	return ''.join(lines)

def author_firstnames_surnames(text):
	soup = BeautifulSoup(text, 'html.parser')
	lines = [
		line for line in [
			line.strip() for line in soup.get_text().split('\n')
		] if len(line)
	]
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
	return '\n  '.join(json.dumps(authors,indent=2).split('\n'))

