import re
from bs4 import BeautifulSoup

def listoflists_to_textlist(listoflists, level = 0):
	s = ""
	for item in listoflists:
		if type(item) is list:
			s += listoflists_to_textlist(item, level+1) + '\n'
		else:
			s += '\n'+('\t'*level)+'- '+str(item)
	if level == 0:
		return s[1:]
	else:
		return s

def htmllist_to_listoflists(text):
	def find_li(element):
		return [{li: find_li(li)}
				for ul in element('ul', recursive=False)
				for li in ul('li', recursive=False)]

	soup = BeautifulSoup(text, 'html.parser')
	return find_li(soup)

# def htmllist_to_listoflists(htmllist, level = 0):
# 	def base_case(listtext):
# 		lst = re.split (
# 			'</li>\s*<li>',
# 			listtext
# 				.replace('<ul>','')
# 					.replace('</ul>','')
# 		)
# 		lst[0]  = re.sub ( '\s*<li>',  '', lst[0]  )
# 		lst[-1] = re.sub ( '</li>\s*', '', lst[-1] )
# 		return lst

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

listtext = """<ul>
    <li>List item one</li>
    <li>List item two with subitems:
        <ul>
            <li>Subitem 1</li>
            <li>Subitem 2</li>
        </ul>
    </li>
    <li>Final list item</li>
</ul>"""
print(
	#listoflists_to_textlist(
		htmllist_to_listoflists(
			listtext
		)
	#)
)

# print(
# 	listoflists_to_stringlist (
# 		[1,
# 			[2, 3, 4],
# 			[1,
# 				[0,0,0],
# 			7],
# 			9
# 		,5]
# 	)
# )
