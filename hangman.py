"""
Author: Bailey Phan
Date: August 23, 2017
Purpose: Simple recreation of hangman in Python
"""
import random 
import ascii
import fonts
import re
import sys
import atexit

MAX_LIVES = len(ascii.hangman) - 1
LINES_PER_GAME = 11
WORDBANK_FILE = 'wordbank.txt'

#loops game until user signals they want to quit
def main():
	#empty lines to be used for game (prevents game from writing over other stuff in terminal)
	for i in range(0,LINES_PER_GAME):
		print()
	#game loop
	keepPlaying = 'y'
	while(keepPlaying == 'y' or keepPlaying == 'yes'):
		playRound()
		keepPlaying = getUserInput('Would you like to keep playing (y/n): ')
		


#Purpose: Plays 1 round of hangman -- picks a word and let user guess until they win/lose
#Inputs: None
#Outputs: None
def playRound():
	#game setup
	lifeCount = [MAX_LIVES]
	guessed = False
	answer = list(retrieveWord()) #convert string to list so it is mutable
	revealed = []
	char_dict = {} #holds characters and their position(s) in string
	user_guesses = [] #all of user's guesses

	#parse word, fill out dictionary, create string that holds revealed chars
	for i in range(0,len(answer)):
		revealed.append('_')
		if answer[i] in char_dict:
			char_dict[answer[i]].append(i)
		else:
			char_dict[answer[i]] = [i]

	#game loop -- exit conditions are out of lives or they guessed the word
	printHangman(spaceRevealed(revealed), lifeCount[0])
	while(lifeCount[0] > 0 and not guessed):
		print()
		guessed = guess(char_dict, revealed, lifeCount, user_guesses)
		printHangman(spaceRevealed(revealed), lifeCount[0])

	print("Characters guessed: " + str(user_guesses).replace("'", "")) #remove single quotes from list

	if(guessed): #they guessed the answer
		printCustomize([fonts.GREEN, fonts.BOLD], "You win!")
	else: #they didnt guess the answer
		printCustomize([fonts.RED, fonts.BOLD], "You lose! The word was: " + ''.join(answer))


#Purpose: Pull a random word from file
#Inputs: None, but WORDBANK_FILE should be set accordingly
#Outputs: None
def retrieveWord():
	try:
		with open(WORDBANK_FILE) as words:
			words = words.readlines()
			someWord = ''
			#make sure there is a list of words and chosen word is 3+ letters
			while(len(words) > 0 and len(someWord) < 2 and not re.match('^[a-zA-Z]+$',someWord)):
				#randomly choose a word from word bank
				someWord = random.choice(words)

				#check if word is valid, if not remove it from word bank
				if len(someWord) < 2 or not re.match('^[a-zA-Z]+$',someWord):
					words.remove(someWord)
				someWord = someWord.lower().rstrip() #lowercase and remove newline

			#no words left in word bank
			if len(words) < 1:
					moveCursorUp(LINES_PER_GAME)
					print("Error: No valid words in \'" + WORDBANK_FILE + "\'")
					sys.exit(0)

			return someWord

	#failed to open file
	except OSError as e:
		moveCursorUp(LINES_PER_GAME)
		print("Error opening wordbank file \'" + WORDBANK_FILE + '\': ' + str(e))
		print("Make sure file exists and run again.")
		sys.exit(0)


	
#Purpose: Takes in user's guess and reveals or reduces lives accordingly
#Inputs: dictionary with mappings of character to list of positions in string, string of previously revealed chars,
#		 integer of how many lives user has, and list of user's previous guesses 
#Outputs: Boolean indicating if they won (True = win, False = loss)
def guess(dictionary, revealed, lives, guesses):

	print("Characters guessed: " + str(guesses).replace("'", "") ) #remove single quotes from list
	
	#get user guess, but make sure they enter a valid character
	user_guess = ''
	while(True):
		user_guess = getUserInput('Guess a character: ')
		if(len(user_guess) >= 1 and re.match('^[a-zA-Z]+$', user_guess) and not user_guess in guesses):
			user_guess = user_guess.lower()[0]
			break
		else:
			moveCursorUp(1)
	
	guesses.append(user_guess) #track their guesses
	if user_guess in dictionary: #they guessed correctly
		#reveal the characters
		for i in dictionary[user_guess]:
			revealed[i] = user_guess
		
		#remove entry from dictionary
		del dictionary[user_guess]

		#if dictionary is empty, they win
		if(not bool(dictionary)):
			return True
		else:
			return False
	else: #they guessed incorrectly
		lives[0]-= 1;
		return False

#Purpose: Inserts a space between characters
#Inputs: Word (string) to be spaced apart
#Outputs: String of word spaced apart
def spaceRevealed(word):
	sb = []
	for c in word:
		sb.append(c + " ")
	return ''.join(sb)

#printing functions

#Purpose: Prints hangman ASCII and revealed characters
#Inputs: String of revealed characters and integer value of lives left
#Outputs: None, but prints to screen
def printHangman(revealedChars, lives):
	hangman_info = ascii.hangman[MAX_LIVES-lives].splitlines()
	halfway = int(len(hangman_info) / 2)
	hangman_info[halfway]+= '\t\t' + fonts.BOLD + revealedChars + fonts.ENDC

	#move cursor up (rewrite over to save space in console)
	moveCursorUp(LINES_PER_GAME)

	for line in hangman_info:
		print(line)
			
#Purpose: Prints text with ansi codes (bold, colors, underline, etc)
#Inputs: List of ansi codes and string of text to be printed
#Outputs: None, but prints text to screen
def	printCustomize(customizations, text):
	sb = []
	#add font modifiers before text
	for customization in customizations:
		sb.append(customization)
	#add text
	sb.append(text)
	#change font back to normal
	sb.append(fonts.ENDC)

	print(''.join(sb))

#cursor manipulation functions

#Purpose: Moves cursor up x lines while clearing text from lines
#Inputs: Integer value of how many lines to move up
#Outputs: None
def moveCursorUp(linesUp):
	#move up while clearing out each line
	for i in range(0,linesUp):
		print("\033[A", end="")
		clearCurrentLine()

#Purpose: Removes text from current line using ansi escape code
#Inputs: None
#Outputs: None
def clearCurrentLine():
	print("\033[K", end='') #ansi code to clear to the end of line

#Purpose: Do things before exit (print thanks for playing)
#Inputs: None
#Outputs: None
def exit_handler():
	print("Thanks for playing!")
atexit.register(exit_handler)

#Purpose: Wrapper for input (handle exceptions)
#Inputs: String for input prompt
##Outputs: String of user input
def getUserInput(prompt):
	try:
		return input(prompt)
	except:
		print()
		sys.exit(0)

if __name__ == "__main__":
	main()
	