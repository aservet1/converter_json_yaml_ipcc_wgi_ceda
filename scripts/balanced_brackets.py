from sys import argv

with open(argv[1]) as f:
	data = list(f.read())

stack = list()

for c in data:
	if c == '[': stack.append('x')
	if c == ']': stack.pop()

print(stack)
