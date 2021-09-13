import re
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

# esta funcion era un lio para hacer.......jajajajajaj
def html_data_to_text(html):
	def htmllist_to_textlist(htmllist):
		def get_single_key(dct):   return list(dct.keys())[0]
		def get_single_value(dct): return list(dct.values())[0]

		def parsedlist_to_plaintextlist(parsedlist, level = 0):
			BULLET = ('\t'*level)+'- '
			text = str()
			for item in parsedlist:
				if type(item) is dict:
					text += (
						BULLET + get_single_key(item) + '\n' +
						parsedlist_to_plaintextlist (
							get_single_value(item),
							level+1
						)
					)
				else:
					text += BULLET + str(item) + '\n'
			return text

		def parse_nested_html_list(text):
			def strip_list_content_and_tags(item):
				item = str(item)
				if '\n' in item:
					item = ' '.join(item.split('\n'))
				item = re.sub('<ul>.*</ul>','',item)
				item = item.replace('<li>','').replace('</li>','')
				return item.strip()

			def find_li(element):
				return [
					{li: find_li(li)}
						for ul in element('ul', recursive=False)
						for li in ul('li', recursive=False)
				] # source: https://stackoverflow.com/questions/24216263/converting-html-list-to-nested-python-list

			def post_processing_find_li_dict_instance(x):
				if not len(get_single_value(x)):
					return strip_list_content_and_tags(get_single_key(x))
				else:
					title = strip_list_content_and_tags(get_single_key(x))
					processed = {title:[]}
					for item in get_single_value(x):
						processed[title].append(post_processing_find_li_dict_instance(item))
					return processed

			soup = BeautifulSoup(text, 'html.parser')
			processed = []
			for item in find_li(soup):
				processed_item = post_processing_find_li_dict_instance(item)
				if type(processed_item) is list:
					processed.extend(processed_item)
				else:
					processed.append(processed_item)
			return processed

		return (
			parsedlist_to_plaintextlist (
				parse_nested_html_list (
					htmllist
				)
			)
		)

	def get_list_part_of_html(html):
		start_idx = 0
		stop_idx  = len(html)

		opener = '<ul>'
		closer = '</ul>'

		while (
			start_idx < stop_idx
				and
			not html[start_idx:start_idx+len(opener)] == opener
		): start_idx += 1
		while (
			stop_idx  > start_idx
				and
			not html[stop_idx-len(closer):stop_idx] == closer
		): stop_idx  -= 1

		return html[start_idx:stop_idx]
	
	listpart = get_list_part_of_html(html)
	processed = (
		BeautifulSoup(
			html.replace(
				listpart,
				htmllist_to_textlist(listpart)
			),
			'html.parser'
		).get_text()
			.strip()
	)
	return '  ' + '\n  '.join(
		'\\n\n'.join(
			processed.split('\n')
		).split('\n')
	)	.strip()