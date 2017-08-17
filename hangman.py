"""
Author: Bailey Phan
Date: August 17, 2017
Purpose: Simple recreation of hangman in Python
"""
import random 

def main():
	#game setup
	lifeCount = [6]
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
	while(lifeCount[0] > 0 and not guessed):
		printRevealed(revealed)
		guessed = guess(char_dict, revealed, lifeCount)

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

		print("Correct!")

		#if dictionary is empty, they win
		if(not bool(dictionary)):
			return True
		else:
			return False
	else: #they guessed incorrectly
		lives[0]-= 1;
		print("Incorrect! Lives: " + str(lives))
		return False

def printRevealed(word):
	for c in word:
		print(c,end=" ")


if __name__ == "__main__":
	main()
	