#!/usr/bin/env python3

import json
from sys import argv
from bs4 import BeautifulSoup
import colors
import os

def newname(fname):
	return fname.split('/')[-1].replace('.json','_field_ds_authors.html')

def blueprint(msg):
	print(colors.BLU+msg+colors.RESET)

src_dir = '../examples/'
dest_dir = 'field_ds_author_fields/'
files = [
	src_dir+ffile
		for ffile in os.listdir(src_dir)
		if ffile.endswith('.json')
]
for filename in files:
	blueprint(filename)
	with open(filename) as ifd:
		with open(dest_dir+newname(filename),'w') as ofd:
			ofd.write(
				json.load(ifd)[0]['field_ds_authors']
			)

# soup = BeautifulSoup(text, "html.parser")
# print(
# 	soup.div
# )
