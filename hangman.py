"""
Author: Bailey Phan
Date: August 17, 2017
Purpose: Simple recreation of hangman in Python
"""
import random 
import ascii
import fonts

MAX_LIVES = len(ascii.hangman) - 1

def main():
	#game setup
	lifeCount = [MAX_LIVES]
	guessed = False
	answer = list(retrieveWord()) #convert string to list so it is mutable
	revealed = []
	char_dict = {} #holds characters and their position(s) in string

	#parse word, fill out dictionary, create string that holds revealed chars
	for i in range(0,len(answer)-1):
		revealed.append('_')
		if answer[i] in char_dict:
			char_dict[answer[i]].append(i)
		else:
			char_dict[answer[i]] = [i]

	#game loop -- exit conditions are out of lives or they guessed the word
	printHangman(spaceRevealed(revealed),lifeCount[0])
	while(lifeCount[0] > 0 and not guessed):
		#printRevealed(revealed)
		print('****************************************')
		guessed = guess(char_dict, revealed, lifeCount)
		printHangman(spaceRevealed(revealed),lifeCount[0])


	if(guessed): #they guessed the answer
		print("You win! You guessed the word: " + ''.join(answer))
	else: #they didnt guess the answer
		print("You lose! The word was: " + ''.join(answer))
	
def retrieveWord():
	lines = open("wordbank.txt").readlines()
	return random.choice(lines)
	
def guess(dictionary, revealed, lives):

	user_guess = input('Guess a character: ')
	if user_guess in dictionary: #they guessed correctly
		#reveal the characters
		for i in dictionary[user_guess]:
			revealed[i] = user_guess
		
		#remove entry from dictionary
		del dictionary[user_guess]

		printCustomize([fonts.GREEN,fonts.BOLD],"CORRECT!")

		#if dictionary is empty, they win
		if(not bool(dictionary)):
			return True
		else:
			return False
	else: #they guessed incorrectly
		lives[0]-= 1;
		#print(fonts.RED + fonts.BOLD + "Incorrect!" + fonts.ENDC)
		printCustomize([fonts.RED,fonts.BOLD], "INCORRECT!")
		return False

def spaceRevealed(word):
	sb = []
	for c in word:
		sb.append(c + " ")
	return ''.join(sb)

def printHangman(revealedChars, lives):
	hangman_info = ascii.hangman[MAX_LIVES-lives].splitlines()
	halfway = int(len(hangman_info) / 2)
	hangman_info[halfway]+= '\t\t' + fonts.BOLD + revealedChars + fonts.ENDC
	#hangman_info[halfway+1]+= '\t\t' + "Lives: " + str(lives)
	for line in hangman_info:
		print(line)
			
	#print(''.join(hangman_info))

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





if __name__ == "__main__":
	main()
	