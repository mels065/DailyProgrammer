class Game
	def battle(word1, word2)
		word1.downcase!
		word2.downcase!
		
		word1.each_char do |c|
			if word2.include?(c)
				w1_i = word1.index(c)
				w2_i = word2.index(c)
				word1 = word1[0...w1_i] + word1[w1_i+1...word1.length]
				word2 = word2[0...w2_i] + word2[w2_i+1...word2.length]
			end
		end
		
		return [word1, word2]
	end
end