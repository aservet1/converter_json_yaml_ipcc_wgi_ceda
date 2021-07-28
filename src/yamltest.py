#!/usr/bin/env python3
import yaml
from sys import argv

try:
	infile = argv[1]
	outfile = argv[2]
except IndexError:
	print("usage:",argv[0],"infile, outfile")

with open(infile) as fd:
	data = yaml.load(fd)

with open(outfile,'w') as fd:
	fd.write(yaml.dump(data,indent=2))
