# Import packages
from Bot import *
from json import load, dumps

class Game:
	'''This class describes the TicTacToe game

	Attributes
	----------
	botModes : Dict[str, func]
	width : int
		The board width
	height : int
		The board height
	board : List[List[bool]]
		The game board
	turn : bool
		Whether it is player1's turn
	gameOver : bool
		Whether the game is over
	remainingCells : Set[int]
		The set of cells that are still empty

	Methods
	-------
	__init__() -> None
		Initializes the Game instance
	makeMove(Tuple[int, int]) -> bool
		Makes a move on the game board and returns if it is successful
	checkWin(Tuple[int, int]) -> bool
		Checks if the game is over
	'''

	botModes = {
		'e': easyBot,
		'm': mediumBot,
		'h': hardBot
	}

	def __init__(self, width, height):
		'''Initializes the Game instance

		Parameters
		----------
		width : int
			The board width
		height : int
			The board height
		'''

		# Initialize values
		self.width = width
		self.height = height
		self.turn = True
		self.gameOver = False

		# Create game board and remainingCells set
		self.board = []
		self.remainingCells = set()
		for x in range(self.width):
			self.board.append([])
			for y in range(self.height):
				self.board[x].append(None)
				self.remainingCells.add((x, y))
	
	def makeMove(self, cell):
		'''Makes a move on the game board and returns if it is successful

		Parameters
		----------
		cell : Tuple[int, int]
			The cell that we want to make a move on
		
		Returns
		-------
		bool
			Whether the move was successful
		'''

		# Check if cell is empty
		if cell not in self.remainingCells:
			return False
		
		# Update the game board
		self.board[cell[1]][cell[0]] = self.turn
		self.remainingCells.remove(cell)

		# Check for a win
		self.gameOver = self.checkWin(cell)

		# Swap turn and return True
		self.turn = not self.turn
		
		return True

	def checkWin(self, lastMove):
		'''Check if the game is over

		Parameters
		----------
		lastMove : Tuple[int, int]
			The last move
		
		Returns
		-------
		bool
			Whether the game is over
		'''

		# Get individual coordinates
		x, y = lastMove

		# Check the row of the cell
		for i in range(1, self.width):
			if self.board[y][0] != self.board[y][i]:
				break
		else:
			return True
		
		# Check the column of the cell
		for i in range(1, self.height):
			if self.board[0][x] != self.board[i][x]:
				break
		else:
			return True
		
		# Check the diagonals if the cell is in them
		# Only applies to squares
		if self.width == self.height and x == y:
			for i in range(1, self.width):
				if self.board[0][0] != self.board[i][i]:
					break
			else:
				return True
		if self.width == self.height and (self.width - x - 1) == y:
			for i in range(1, self.width):
				if self.board[0][self.width - 1] != self.board[i][self.width - i - 1]:
					break
			else:
				return True

		# There are no matches
		return False

if __name__ == '__main__':
	# Runs if this file is run directly
	displayMap = {
		None: '_',
		False: 'O',
		True: 'X'
	}

	# Run as long as the user wants to play a game
	while True:
		# Take input parameters
		botEnabled = input('Single Player / Double Player - S/D: ').lower() == 's'
		if botEnabled:
			mode = input('Enter your difficulty mode - E/M/H: ')
			bot = Game.botModes[mode.lower()]
			names = [
				input('Enter the Player\'s name: '),
				'the computer'
			]
			player = int(input('Enter which player you want to be: '))
		else:
			names = [
				input('Enter Player 1\'s name: '),
				input('Enter Player 2\'s name: ')
			]
			player = 1
		width, height = map(int, input('Enter board dimensions: ').split())
		game = Game(width, height)
		print()
		
		# Run the game
		while not game.gameOver and len(game.remainingCells) > 0:
			print(f'It is {names[not game.turn]}\'s turn')

			if (not botEnabled) or 1 + (not game.turn) == player:
				# It is the players turn
				# Get move input
				x, y = map(int, input('Enter cell: ').split())
				if not game.makeMove((x - 1, y - 1)):
					print('Not a valid move. Try again')
					continue
				
				# Display the board
				print('Board:')
				for row in game.board:
					print(*map(lambda x: displayMap[x], row))
				print()
			else:
				# It is the bots turn
				move = bot(game)
				game.makeMove(move)

				# Display the board
				print('Board:')
				for row in game.board:
					print(*map(lambda x: displayMap[x], row))
				print()

		# Display the result
		if game.gameOver:
			if botEnabled and 1 + game.turn != player:
				print(f'The computer won!')
			else:
				print(f'{names[game.turn]} won!')

			# get player scores
			if True:
				scoresDict = {}
				try:
					with open('scores.json', 'r') as scoresFile:
						scoresDict = load(scoresFile)
				except:
					# File has not been created
					pass
	
				# add players to scoresDict if not already present
				if names[game.turn] not in scoresDict:
					scoresDict[names[game.turn]] = {
						'win': 0,
						'lose': 0,
						'draw': 0
					}
				if names[not game.turn] not in scoresDict:
					scoresDict[names[not game.turn]] = {
						'win': 0,
						'lose': 0,
						'draw': 0
					}

				# update scores in scores.json
				if game.gameOver:
					scoresDict[names[game.turn]]['win'] += 1
					scoresDict[names[not game.turn]]['lose'] += 1
				else:
					scoresDict[names[game.turn]]['draw'] += 1
					scoresDict[names[not game.turn]]['draw'] += 1

				scoresDict.pop('the computer', None)

				# save results to scores.json
				with open('scores.json', 'w') as scoresFile:
					scoresFile.write(dumps(scoresDict))
		else:
			print('It is a draw')
		print('Thank you for playing!')

		# Check if the user wants to play again		
		if not input('Press <Enter> to exit and any other key to play again: '):
			break
		print()
