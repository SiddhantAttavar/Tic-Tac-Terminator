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


def hardBot(game):
	'''Returns the move for the hard mode bot

	This method implements the minimax algorithm

	Parameters
	----------
	game : Game
		The current game board
	
	Returns
	-------
	Tuple[int, int]
		The next move of the hard bot
	'''
	
	# Initialize variables
	emptyCells = list(game.remainingCells)
	player = game.turn
	res = -1
	bestMove = emptyCells[0]

	# Iterate throught moves and find the best one
	for x, y in emptyCells:
		# Try selecting the cell
		game.board[y][x] = player
		game.remainingCells.remove((x, y))

		# Get the best move
		curr = hardBotUtil(player, not player, game)
		if curr > res:
			res = curr
			bestMove = (x, y)
		
		# Revert to previous turn
		game.board[y][x] = None
		game.remainingCells.add((x, y))
	
	# Returns the best move
	return bestMove


def hardBotUtil(player, currPlayer, game):
	'''Implements the minimax algorithm

	Parameters
	----------
	player : bool
		The initial player
	game : Game
		The current game state
	
	Returns
	-------
	int
		The score
	'''

	# Calculate score
	score = evaluateBoard(player, game.board, game.width, game.height)

	# Check for whether the game is over
	if score != 0 or len(game.remainingCells) == 0:
		return score
	
	# Recursively travel through game tree
	res = -1 if currPlayer == player else 1
	emptyCells = list(game.remainingCells)
	for x, y in emptyCells:
		# Try selecting the cell
		game.board[y][x] = currPlayer
		game.remainingCells.remove((x, y))

		# Get the best move
		curr = hardBotUtil(player, not currPlayer, game)
		if currPlayer == player:
			res = max(res, curr)
		else:
			res = min(res, curr)
		
		# Revert to previous turn
		game.board[y][x] = None
		game.remainingCells.add((x, y))
	
	# Return the score
	return res

def evaluateBoard(player, board, width, height):
	'''Returns the score of the board

	-1: Losing state
	0: Draw state
	1: Winning state

	Parameters
	----------
	player : bool
		The initial player
	board : List[List[int]]
		The current game board
	width : int
		The width of the game board
	height : int
		The height of the game board
	
	Returns
	-------
	int
		The score
	'''
	
	# Check rows
	for x in range(width):
		if board[0][x] == None:
			continue

		for y in range(1, height):
			if board[y][x] != board[0][x]:
				break
		else:
			if board[0][x] == player:
				return 1
			else:
				return -1
	
	# Check columns
	for y in range(height):
		if board[y][0] == None:
			continue

		for x in range(1, width):
			if board[y][x] != board[y][0]:
				break
		else:
			if board[y][0] == player:
				return 1
			else:
				return -1
	
	# Check diagonals if applicable
	if width != height:
		return 0
	
	# Top-left to Bottom-right
	for j in range(1, width):
		if board[j][j] != board[0][0]:
			break
	else:
		if board[0][0] == player:
			return 1
		else:
			return -1
	
	# Top-right to Bottom-left
	for j in range(1, width):
		if board[j][width - j - 1] != board[0][width - 1]:
			break
	else:
		if board[0][width - 1] == player:
			return 1
		else:
			return -1
	
	# It is a draw situation
	return 0
