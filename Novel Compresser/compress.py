import re
from decompress import Compresser

WORD_RE = re.compile(r"[A-Za-z]+")
SYMBOL_RE = re.compile(r"[\.,\?!;:]")
LOWER_WORD_RE = re.compile(r"[a-z]+")
CAP_WORD_RE = re.compile(r"[A-Z][a-z]*")
UPPER_WORD_RE = re.compile(r"[A-Z][A-Z]+")
HYPHEN_WORD_RE = re.compile(r"([a-z]+|[A-Z][a-z]+|[A-Z]+)+-(\1-*)*")
SYMBOL_WORD_RE = re.compile(r"([a-z]+|[A-Z][a-z]+|[A-Z]+)[\.,\?!;:]")

ERROR_RE = re.compile(r"([a-z]+[A-Z]+|[[A-Z][A-Z]+[a-z]+]|[0-9]+|[\.,\?!;:][\.,\?!;:]+|[^a-zA-Z\.,\?!;:\-]|^-)")

class Compresser(Compresser):
	def compress(self):
		regular_text = ""
	
		print "Type text and use EOF symbol to end: "
		
		while True:
			try:
				if len(regular_text) == 0:
					regular_text += raw_input()
				else:
					regular_text += '\n' + raw_input()
			except EOFError:
				break
				
		index = 0
		end_index = 0
		while end_index != -1:
			end_index = regular_text.find('\n', index)
			if end_index != -1:
				line = regular_text[index:end_index].split()
			else:
				line = regular_text[index:len(regular_text)].split()
				
			for word in line:
				if ERROR_RE.search(word):
					print "Invalid text input: terminating process"
					return
				elif HYPHEN_WORD_RE.search(word) or SYMBOL_WORD_RE.search(word):
					self.hyphen_and_symbol_word_handler(word)
				else:
					self.regular_word_handler(word)
			
			if end_index != -1:
				self.text += 'R '
			else:
				self.text += 'E '
			
			index = end_index + 1
			
	def hyphen_and_symbol_word_handler(self, word):
		index = 0
		while index < len(word):
			if word[index] == '-':
				self.text += '- '
				index += 1
			elif SYMBOL_RE.search(word, index, index + 1):
				self.text += word[index] + ' '
				index += 1
			else:
				sub_word = WORD_RE.search(word, index)
				if sub_word:
					self.regular_word_handler(sub_word.group(0))
					index += len(sub_word.group(0))
				else:
					index += 1
				
	def regular_word_handler(self, word):
		if word.lower() not in self.dict:
			self.dict.append(word.lower())
		
		if CAP_WORD_RE.search(word):
			self.text += str(self.dict.index(word.lower())) + '^ '
		elif UPPER_WORD_RE.search(word):
			self.text += str(self.dict.index(word.lower())) + '! '
		else:
			self.text += str(self.dict.index(word.lower())) + ' '
		
	def read_dict(self):
		print len(self.dict)
		for word in self.dict: print word
		
	def run_compress(self):
		self.clear()
		
		self.compress()
		
		self.read_dict()
		self.read_text()
	
if __name__ == "__main__":
	c = Compresser()
	c.run_compress()