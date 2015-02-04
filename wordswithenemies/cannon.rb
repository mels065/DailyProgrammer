class Game
	private
	
	@word1 = ""
	@word2 = ""
	
	def battle(word1, word2)
		@word1 = word1.downcase
		@word2 = word2.downcase
		
		@word1.each_char do |c|
			if @word2.include?(c)
				w1_i = @word1.index(c)
				w2_i = @word2.index(c)
				@word1 = @word1[0...w1_i] + @word1[w1_i+1...word1.length]
				@word2 = @word2[0...w2_i] + @word2[w2_i+1...word2.length]
			end
		end
	end
	
	def result
		puts @word1 + @word2
		if @word1.length > @word2.length
			puts "Word 1 wins!"
		elsif @word1.length < @word2.length
			puts "Word 2 wins!"
		else
			puts "It's a tie!"
		end
		puts
	end
	
	public
	
	def run
		puts "Welcome to Words with Enemies!"
		puts
		
		loop do
			puts "Type in two words separated by a space"
			print "If you want to quit, type in q: "
			user_input = gets.chomp
			
			if user_input.downcase == 'q'
				break
			elsif /^[a-zA-Z]+ [a-zA-Z]+$/.match(user_input)
				words = user_input.split
				battle(words[0], words[1])
				result
			else
				puts "Invalid input!"
				puts
			end
		end
	end
end

game = Game.new
game.run
