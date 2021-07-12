#!/usr/bin/env python3
import yaml
from sys import argv


print(yaml.dump(yaml.load(open(argv[1])),open(argv[2],'w'),indent=2))
