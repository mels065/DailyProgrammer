from collections import OrderedDict

INPUT_FILE = "enable1.txt"
OUTPUT_FILE = "hackwords.txt"

def format():
	dict = OrderedDict()
	for i in range(4, 16):
		dict[i] = []
	
	with open(INPUT_FILE) as input_file:
		line = input_file.readline()
		while len(line) > 0:
			length = len(line) - 1
			if length in dict.keys(): dict[length].append(line)
			line = input_file.readline()
	input_file.closed
	
	with open(OUTPUT_FILE, 'w') as output_file:
		for i in dict.keys():
			output_file.write(str(i) + '\n')
			for word in dict[i]: output_file.write(word)
	output_file.closed
	
format()