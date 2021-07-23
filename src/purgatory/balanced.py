from sys import argv

with open(argv[1]) as f:
	data = list(f.read())
opener = argv[2]
closer = argv[3]

stack = list()

print(f"opener:{opener}\ncloser:{closer}")

for c in list(data):
	if c == opener:
		print('push')
		stack.append('x')
	if c == closer:
		print('pop')
		stack.pop()

print(stack)
