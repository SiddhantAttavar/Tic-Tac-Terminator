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

def mediumBot(game):
	'''Returns the move for the medium mode bot

	This bot selects any immediate possibility of a win.
	If this is not possible, it tries to block any immediate possibility of a loss.
	Otherwise, it selects a random cell

	Parameters
	----------
	game : Game
		The current game board
	
	Returns
	-------
	Tuple[int, int]
		The next move of the medium bot
	'''

	# Check if any cell will provide an immediate win
	emptyCells = list(game.remainingCells)
	for x, y in emptyCells:
		# Try selecting the cell
		game.makeMove((x, y))
		
		# Revert to previous turn
		game.board[y][x] = None
		game.remainingCells.add((x, y))
		game.turn = not game.turn

		# Check if this cell is an immediate win
		if game.gameOver:
			game.gameOver = False
			return (x, y)

	# Check if any cell will block an immediate opponent win
	if len(emptyCells) > 1:
		game.turn = not game.turn
		for x, y in emptyCells:
			# Try selecting the cell
			game.makeMove((x, y))
			
			# Revert to previous turn
			game.board[y][x] = None
			game.remainingCells.add((x, y))
			game.turn = not game.turn

			# Check if this cell blocks anything
			if game.gameOver:
				game.gameOver = False
				game.turn = not game.turn
				return (x, y)
		game.turn = not game.turn
	
	# Select a random cell from game.remainingCells
	return choice(emptyCells)
