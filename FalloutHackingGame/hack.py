import random
import re

DICT_FILE = "hackwords.txt"
DIFFICULTY_LENGTH = {1: [4],
					 2: [5, 6, 7],
					 3: [7, 8, 9],
					 4: [10, 11, 12],
					 5: [13, 14, 15]}
					 
DIGIT_RE = re.compile(r'\d+')

class Hacker:
	def __init__(self):
		self.difficulty = None
		self.guesses = None
		self.words = []
		self.secret = ""
		
	def new_game(self, difficulty):
		self.guesses = 4
		self.words = []
		
		with open(DICT_FILE) as file:
			file_text = file.read()
		file.closed
		
		self.difficulty = difficulty
		length = random.choice(DIFFICULTY_LENGTH[difficulty])
		
		#File is organized by the length of the words;
		#Find the length index and the index of the following
		#length index
		index = file_text.find(str(length))
		end_index = file_text.find(DIGIT_RE.search(file_text, index + len(str(length))).group(0),
		index + 1)
		
		dict = file_text[index + len(str(length)):end_index].split('\n')
		
		num_of_words = random.randrange(5, 16)
		for i in range(num_of_words):
			word = random.choice(dict).upper()
			while word in self.words and len(word) <= 0: word = random.choice(dict).upper()
			self.words.append(word)
			
		self.secret = random.choice(self.words)
			
	def run(self):
		input = ''
		while input != 'N':
			input = raw_input('Difficulty (1-5)? ')
			while not input.isdigit() or \
			int(input) not in DIFFICULTY_LENGTH.keys():
				input = raw_input('Difficulty (1-5)? ')
			
			self.new_game(int(input))
			
			for word in self.words:
				print word
			
			win = False
			while self.guesses > 0:
				correct = 0
				input = raw_input("Guess (%s left)? " % str(self.guesses)).upper()
				if input not in self.words:
					print "Invalid word!"
					continue
				
				
				for i in range(len(self.secret)):
					if self.secret[i] == input[i]: correct += 1
				
				print "%s/%s correct" % (correct, len(self.secret))
				if correct == len(self.secret):
					print "You win!\n"
					win = True
					break
					
				self.guesses -= 1
			
			if not win:
				print "Terminal has locked!\n"
				
			input = raw_input("Play again? (Y/N): ").upper()
			while not re.compile(r'^[YN]$').search(input):
				input = raw_input("Play again? (Y/N): ").upper()
			
if __name__ == '__main__':
	hack = Hacker()
	hack.run()