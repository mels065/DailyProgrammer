import re

#Constants for regexp
ENTRY = re.compile(r"[0-9]+")
CAP_ENTRY = re.compile(r"[0-9]+\^")
UP_ENTRY = re.compile(r"[0-9]+\!")
SYMBOL_ENTRY = re.compile(r"[\.,\?!;:]")

class Compresser:
	def __init__(self):
		self.dict = []
		self.text = ""
	
	#Prompts user to add an amount of words equal to the number
	#they entered at the beginning of prompt
	def add_to_dict(self, num_of_entries):
		print "Now enter a word on each line that will go in the dictionary."
		for i in range(num_of_entries):
			word = raw_input()
			self.dict.append(word)
	
	#User can enter words based on dictionary
	def decompress(self):
		last_input = ""
		print "Now use the appropriate commands to enter text (Read the manual to understand the codes):"
		
		while last_input.upper() != "E":
			line = raw_input().split()
			hyphenate = False
			for cmd in line:
				last_input = cmd
				
				if CAP_ENTRY.search(cmd):
					self.text += self.dict[int(cmd.strip('^'))].capitalize()
				elif UP_ENTRY.search(cmd):
					self.text += self.dict[int(cmd.strip('!'))].upper()
				elif ENTRY.search(cmd):
					self.text += self.dict[int(cmd)]
				elif cmd == '-':
					hyphenate = True
				elif SYMBOL_ENTRY.search(cmd):
					self.text += '\b' + cmd
				elif cmd.upper() == 'R':
					self.text += '\n'
					continue
				elif cmd.upper() == 'E':
					break
				else:
					print "Invalid entry on the line!"
					break
				
				if hyphenate:
					self.text += '-'
					hyphenate = False
				else:
					self.text += ' '
	
	#Read text back to user
	def read_text(self):
		print self.text
	
	#Empty current dictionary
	def clear_dict(self):
		self.dict = []
	
	#Empty the current text
	def clear_text(self):
		self.text = ""
	
	#Clear all values
	def clear(self):
		self.clear_dict()
		self.clear_text()
	
	#Run the program
	def run_decompress(self):
		self.clear()
		num_of_entries = int(raw_input("Please enter the number of dictionary entries: "))
		
		self.add_to_dict(num_of_entries)
		
		self.decompress()
		self.read_text()
		
if __name__ == '__main__':
	c = Compresser()
	c.run_decompress()