'''This file contains the functions for different bots:
 - Easy mode
 - Medium mode
 - Hard mode

Methods
-------
easyBot(board) -> Tuple[int, int]
	Returns the move for the easy mode bot
mediumBot(board) -> Tuple[int, int]
	Returns the move for the medium bot
hardBot(board) -> Tuple[int, int]
	Returns the move for the hard bot
'''

# Import required packages
from random import choice
from copy import deepcopy

def easyBot(game):
	'''Returns the move for the easy mode bot

	This method randomly chooses an empty cell

	Parameters
	----------
	game : Game
		The current game board
	
	Returns
	-------
	Tuple[int, int]
		The next move of the easy bot
	'''

	# Select a random cell from game.remainingCells
	return choice(list(game.remainingCells))
