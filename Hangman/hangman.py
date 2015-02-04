import random
import re

DEBUG = False
FILENAME = "wordlist.txt"
HANGMAN_STATE_BOARD = {0: "  --------\n" + \
                          "  |      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       1: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       2: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          "  |      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       3: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          "  |      |\n" + \
                          "  |      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       4: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          " /|      |\n" + \
                          "  |      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       5: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          " /|\     |\n" + \
                          "  |      |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       6: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          " /|\     |\n" + \
                          "  |      |\n" + \
                          " /       |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------",
                       7: "  --------\n" + \
                          "  |      |\n" + \
                          "  O      |\n" + \
                          " /|\     |\n" + \
                          "  |      |\n" + \
                          " / \     |\n" + \
                          "         |\n" + \
                          "         |\n" + \
                          "-------------------"}

keep_playing = True
game_state = 0
long_word_len = 0
win = False
used_choices = []

def get_words():
    global long_word_len
    words = {}
    with open(FILENAME, 'r') as f:
        for line in f:
            word = "".join(re.split(re.compile(r'[^a-zA-Z]'), line))

            if DEBUG and len(word) == 4:
                print line[:len(line)-1], word
                
            if len(word) > long_word_len:
                long_word_len = len(word)
            if len(word) not in words:
                words[len(word)] = []
            words[len(word)].append(word.upper())
    f.closed
    return words

def reset_game():
    global game_state, win, used_choices
    game_state = 0
    win = False
    used_choices = []

def print_game_state(current_reveal, secret_word):
    print HANGMAN_STATE_BOARD[game_state]
    print '\n'
    print current_reveal
    print '\n'
    print "".join(["Used Letters: ", str(used_choices)])
    if DEBUG:
        print secret_word

def play_game():
    global keep_playing, game_state, win, used_choices
    words = get_words()
    while True:
        while True:
            print "Which difficulty setting will you pick?"
            choice = raw_input("(Easy[1], Medium[2], Hard[3], Quit[Q]): ")
            if choice == '1' or choice.capitalize() == 'Easy':
                word_len = range(3,6)
                break
            elif choice == '2' or choice.capitalize() == 'Medium':
                word_len = range(5,8)
                break
            elif choice == '3' or choice.capitalize() == 'Hard':
                word_len = range(7, long_word_len + 1)
                break
            elif choice.upper() == 'Q' or choice.capitalize() == 'Quit':
                keep_playing = False
                break
            else:
                print "Invalid input!"

        if not keep_playing:
            break
        
        secret_word = random.choice(words[random.choice([x for x in word_len if x in words.keys()])])
        current_reveal = ' _' * len(secret_word)
        print_game_state(current_reveal, secret_word)
        
        while game_state < 7:
            while True:
                choice = raw_input("Pick a letter: ")
                if choice in used_choices:
                    print "You've already used that letter!"
                elif re.compile(r'[a-zA-Z]').search(choice) and len(choice) == 1:
                    choice = choice.upper()
                    break
                else:
                    print "Invalid input!"
            if choice in secret_word:
                for i in range(0, len(secret_word)):
                    if secret_word[i] == choice:
                        current_reveal = ''.join([current_reveal[:i*2+1], choice, current_reveal[i*2+2:]])
            else:
                game_state += 1

            used_choices.append(choice)
            print_game_state(current_reveal, secret_word)

            if '_' not in current_reveal:
                win = True
                break

        if win:
            print "You win!"
        else:
            print "You were hanged! Game over!"
            print "The word was:", secret_word

        while True:
            choice = raw_input("Play again? (Yes[Y], No[N]): ")
            if choice.upper() == 'Y' or choice.capitalize() == 'Yes':
                keep_playing = True
                break
            elif choice.upper() == 'N' or choice.capitalize() == 'No':
                keep_playing = False
                break

        if not keep_playing:
            break

        reset_game()

if __name__ == '__main__':
    play_game()
