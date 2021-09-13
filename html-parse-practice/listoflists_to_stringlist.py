import re
from bs4 import BeautifulSoup

# 	listoflists = []
# 	i = 0
# 	while (i < len(htmllist)):
# 		if htmllist[i:].startswith("<ul>"):
# 			length_captured, level_down = htmllist_to_listoflists(htmllist[i+len("<ul>"):], level+1)
# 			i += length_captured
# 			listoflists.append(level_down)

# 		elif htmllist[i:].startswith("</ul>"):
# 			top_level_list = htmllist[:i+len("</ul>")]
# 			return len(top_level_list), base_case(top_level_list)
# 		else:
# 			i += 1

# 	if level == 0:
# 		return listoflists
# 	else:
# 		return len(htmllist), listoflists

def html_data_list_to_text(html):

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
	return (
		'\\n\n'.join(
			processed.split('\n')
		)
	)

# listtext = \
# """
# <ul>
#     <li>List item one</li>
#     <li>Title
#         <ul>
#             <li>Subitem 1</li>
#             <li>Subitem 2</li>
#         </ul>
#     </li>
#     <li>Final list item</li>
# </ul>
# """

# TODO remember to consider text strings that don't have any <ul></ul> portions
html = """
<p> Some pre-list text </p>
<ul>
  <li>Morning Kumquat Delicacies
  <ul>
    <li>Hot Dishes
    <ul>
      <li>Kumquat omelet</li>
      <li>Kumquat waffles
      <ul>
        <li>Country style</li>
        <li>Belgian</li>
      </ul>
      </li>
      <li>Kumquats and toast</li>
     </ul>
    </li>
    <li>Cold Dishes
    <ul>
      <li>Kumquats and cornflakes</li>
      <li>Pickled Kumquats</li>
      <li>Diced Kumquats</li>
    </ul>
   </li>
  </ul>
 </li>
</ul>
"""

print(html_data_list_to_text(html))
