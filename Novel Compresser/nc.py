import re
import sys
import os

from decompress import (ENTRY,
						CAP_ENTRY, 
						UP_ENTRY, 
						SYMBOL_ENTRY)
from compress import (WORD_RE,
					  SYMBOL_RE,
					  LOWER_WORD_RE,
					  CAP_WORD_RE,
					  UPPER_WORD_RE,
					  HYPHEN_WORD_RE,
					  SYMBOL_WORD_RE,
					  ERROR_RE)

from compress import Compresser

FIRST_ARG = re.compile(r"-[cdCD]")
SECOND_THIRD_ARG = re.compile(r"\w+\.txt")

CURRENT_DIR = os.getcwd().replace('\\', '/') + '/'

class Compresser(Compresser):
	def decompress(self, input):
		index = 0
		end_index = 0
		while end_index != -1:
			end_index = input.find('\n', index)
			if end_index != -1:
				line = input[index:end_index].split()
			else:
				line = input[index:len(input)].split()
			
			hyphenate = False
			for cmd in line:
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
					return True
				else:
					print "Invalid entry in the text! Terminating process."
					return False
					
				if hyphenate:
					self.text += '-'
					hyphenate = False
				else:
					self.text += ' '
			
			index = end_index + 1
			
		return False
		
	def compress(self, input):
		index = 0
		end_index = 0
		while end_index != -1:
			end_index = input.find('\n', index)
			if end_index != -1:
				line = input[index:end_index].split()
			else:
				line = input[index:len(input)].split()
				
			for word in line:
				if ERROR_RE.search(word):
					print "Invalid text input: terminating process"
					return False
				elif HYPHEN_WORD_RE.search(word) or SYMBOL_WORD_RE.search(word):
					self.hyphen_and_symbol_word_handler(word)
				else:
					self.regular_word_handler(word)
			
			if end_index != -1:
				self.text += 'R '
			else:
				self.text += 'E '
			
			index = end_index + 1
			
		return True
	
	def add_to_dict(self, num_of_entries, entries):
		index = 0
		end_index = 0
		for i in range(num_of_entries):
			end_index = entries.find('\n', index)
			if end_index != -1:
				line = entries[index:end_index].split()
			else:
				print "Not enough entries! Terminating process."
				return False
			
			if len(line) == 1:
				self.dict.append(line[0])
			else:
				print "Invalid entry! Terminating process."
				return False, ""
			
			index = end_index + 1
		
		end_index = entries.find('\n', index)
		if end_index != -1:
			line = entries[index:end_index].split()
		else:
			line = entries[index:len(entries)].split()
		
		if len(line) == 1 and line[0].upper() != 'E':
			print 'Too many entries were given! Terminating process.'
			return False, ""
		
		return True, entries[index:]
		
	def run(self):
		self.clear()
		
		if len(sys.argv) > 4 or len(sys.argv) < 4:
			print "Invalid number of arguments!!"
		elif FIRST_ARG.search(sys.argv[1]) and \
		SECOND_THIRD_ARG.search(sys.argv[2]) and \
		SECOND_THIRD_ARG.search(sys.argv[3]) and \
		sys.argv[2] != sys.argv[3]:
			if sys.argv[1].lower() == '-c':
				input_file = open(sys.argv[2])
				input_text = input_file.read()
				
				success = self.compress(input_text)
				if success:
					output_file = open(sys.argv[3], 'w')
					output_file.write(self.text)
					output_file.close()
				
				input_file.close()
			elif sys.argv[1].lower() == '-d':
				input_file = open(sys.argv[2])
				input_text = input_file.read()
				
				index = input_text.find('\n')
				
				if not ENTRY.search(input_text[:index]):
					print "Invalid entry: Need integer entry!"
					return
					
				num_of_entries = int(input_text[:index])
				success, input_text = self.add_to_dict(num_of_entries, input_text[index + 1:])
				input_file.close()
				
				if not success: return
				
				success = self.decompress(input_text)
				
				if not success: return
				
				output_file = open(sys.argv[3], 'w')
				output_file.write(self.text)
				output_file.close()
				
		else:
			print "Invalid argument entry!!"

if __name__ == "__main__":
	c = Compresser()
	c.run()