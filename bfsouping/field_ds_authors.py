#!/usr/bin/env python3

import json
from sys import argv
from bs4 import BeautifulSoup
import src.colors

fname = 'examples/Fig_3.10.json'
with open(fname) as fd:
	text = json.load(fd)[0]['field_ds_authors']

print(src.colors.BLU,text,src.colors.RESET)

soup = BeautifulSoup(text, "html.parser")
print(
	soup.div
)

