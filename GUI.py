# import necessary packages
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame, sys, time
from Game import Game
from Buttons import Button, TextButton
from json import load, dumps

# set screen dimensions
WIDTH, HEIGHT = 650, 650

# initialize pygame window
pygame.init()
pygame.display.set_caption('Tic Tac Terminator')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
bg_image = pygame.image.load('assets/background.jpg').convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT+100))
font = pygame.font.Font(None, 40)
font_large = pygame.font.Font(None, 60)

# initialize the game
game = Game(3,3)
game_over = False
game_state = 'number_of_players'
player_1_name = TextButton(screen, (WIDTH // 2, HEIGHT // 2))
player_2_name = TextButton(screen, (WIDTH // 2, HEIGHT // 2))

def print_message(message, pos=(WIDTH  //  2, HEIGHT+50), anchor='center', font=font_large):
	'''Displays a message on the screen
	
	Parameters
	----------
	message : str
		The message to be displayed
	pos : tuple
		The position of the message
	anchor : str
		Where the position tuple is to be anchored
	font : pygame.font
		The font of the message
	'''

	text = font.render(message, True, 'darkgreen')
	if anchor == 'center': text_rect = text.get_rect(center = pos)
	elif anchor == 'midleft': text_rect = text.get_rect(midleft = pos)
	screen.blit(text, text_rect)

def draw_board():
	'''Draws the board on the screen'''

	# draw the background image and tic-tac-toe lines
	screen.blit(bg_image, (0,0))
	pygame.draw.line(screen, 'black', (WIDTH/3, 0), (WIDTH/3, HEIGHT), 5)
	pygame.draw.line(screen, 'black', (2*(WIDTH/3), 0), (2*(WIDTH/3), HEIGHT), 5)
	pygame.draw.line(screen, 'black', (0, HEIGHT/3), (WIDTH, HEIGHT/3), 5)
	pygame.draw.line(screen, 'black', (0, 2*(HEIGHT/3)), (WIDTH, 2*(HEIGHT/3)), 5)

	# draw the X's and O's
	for col_ind, col in enumerate(game.board):
		for row_ind, cell in enumerate(col):
			if cell == True:
				surf = pygame.image.load('assets/x.png')
				rect = surf.get_rect(center = (WIDTH // 6 + row_ind*(WIDTH // 3), HEIGHT // 6 + col_ind*(HEIGHT // 3)))
				screen.blit(surf, rect)
			elif cell == False:
				surf = pygame.image.load('assets/o.png')
				rect = surf.get_rect(center = (WIDTH // 6 + row_ind*(WIDTH // 3), HEIGHT // 6 + col_ind*(HEIGHT // 3)))
				screen.blit(surf, rect)


# main loop
# run until user closes the window
while True:

	# event loop
	for event in pygame.event.get():
		# close the window
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# check the game state and run the appropriate screen

	# choose number of players
	if game_state == 'number_of_players':
		# display the background image, prompt and buttons
		screen.blit(bg_image, (0,0))
		print_message('How many players?', (WIDTH  //  2, HEIGHT  //  2 - 100))
		button_1 = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2), '1')
		button_2 = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2 + 100), '2')
		
		# check if any button is clicked
		if button_1.is_clicked():
			game_state = 'player_selection'
			botEnabled = True
			time.sleep(0.2)
		elif button_2.is_clicked():
			game_state = 'player_names'
			botEnabled = False
			time.sleep(0.2)
	
	# choose to play as X or O
	# only runs for single player game
	elif game_state == 'player_selection':
		# display the background image, prompt and buttons
		screen.blit(bg_image, (0,0))
		print_message('Play as', (WIDTH  //  2, HEIGHT  //  2 - 100))
		button_x = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2), 'X')
		button_o = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2 + 100), 'O')
		
		# check if any button is clicked
		if button_x.is_clicked():
			game_state = 'player_names'
			player = 1
			time.sleep(0.2)
		elif button_o.is_clicked():
			game_state = 'player_names'
			player = 2
			time.sleep(0.2)
	
	# enter player names
	elif game_state == 'player_names':
		# display the background image and prompt
		screen.blit(bg_image, (0,0))
		print_message('Press ENTER to continue', font=font)

		# check if single player or double player
		if botEnabled:
			# display the prompt
			print_message('Enter your name', (75, HEIGHT  //  2), 'midleft', font)
			
			# check if user is playing as X or O
			# assign user's name to the appropriate player
			# assign the other player's name as 'the computer'
			if player == 1:
				player_1_name.draw(screen, (WIDTH // 2, HEIGHT // 2 - 25))
				player_1_name.check_active()
				player_1 = player_1_name.get_input()
				player_2 = 'the computer'
			else:
				player_2_name.draw(screen, (WIDTH // 2, HEIGHT // 2 - 25))
				player_2_name.check_active()
				player_2 = player_2_name.get_input()
				player_1 = 'the computer'
		
		# 2 players
		else:
			# get Player 1's name
			print_message('Enter player 1 name', (50, HEIGHT  //  2 - 50), 'midleft', font)
			player_1_name.draw(screen, (WIDTH // 2, HEIGHT // 2 - 75))
			player_1_name.check_active()
			player_1 = player_1_name.get_input()
			
			# get Player 2's name
			print_message('Enter player 2 name', (50, HEIGHT  //  2 + 50), 'midleft', font)
			player_2_name.draw(screen, (WIDTH // 2, HEIGHT // 2 + 25))
			player_2_name.check_active()
			player_2 = player_2_name.get_input()
		
		# assign final names to names list
		names = [player_1, player_2]

		# check if ENTER key is pressed and move to next screen
		if pygame.key.get_pressed()[pygame.K_RETURN]:
			# check for single player or double player
			# if single player, ask for bot difficulty, otherwise start the game
			if botEnabled:
				game_state = 'bot_difficulty'
			else:
				game_state = 'active'

	# choose difficulty of bot
	# only runs for single player game
	elif game_state == 'bot_difficulty':
		# display the background image, prompt and buttons
		screen.blit(bg_image, (0,0))
		print_message('Select difficulty level', (WIDTH  //  2, HEIGHT  //  2 - 100))
		button_e = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2), 'Easy')
		button_m = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2 + 100), 'Medium')
		button_h = Button(screen, (WIDTH  //  2 - 100, HEIGHT  //  2 + 200), 'Hard')
		
		# check if any of the buttons are clicked
		if button_e.is_clicked():
			game_state = 'active'
			bot = Game.botModes['e']
			time.sleep(0.2)
		elif button_m.is_clicked():
			game_state = 'active'
			bot = Game.botModes['m']
			time.sleep(0.2)
		elif button_h.is_clicked():
			game_state = 'active'
			bot = Game.botModes['h']
			time.sleep(0.2)
	
	# the actual game
	elif game_state == 'active':
		# check if game is over
		if not game.gameOver and len(game.remainingCells) > 0:
			# display the board and who's turn it is
			draw_board()
			print_message(f'It is {names[not game.turn]}\'s turn', font=font)
			
			# check if player's turn or bot's turn
			if (not botEnabled) or 1 + (not game.turn) == player:
				if pygame.mouse.get_pressed()[0]:
					# get mouse position and the cell being clicked
					x, y = pygame.mouse.get_pos()
					if x < WIDTH/3: col = 0
					elif x < 2*(WIDTH/3): col = 1
					else: col = 2
					if y < HEIGHT/3: row = 0
					elif y < 2*(HEIGHT/3): row = 1
					else: row = 2

					# try to make the move
					game.makeMove((col, row))

			# bot's turn		
			else:
				move = bot(game)
				game.makeMove(move)
		
		# game is over
		else:
			draw_board()

			if not game_over:
				# get player scores
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

				game_over = True

			# check for win or draw
			if game.gameOver:
				print_message(f'{names[game.turn].capitalize()} won!', (50, HEIGHT+50), 'midleft', font)
			else:
				print_message('It is a draw!', (50, HEIGHT+50), 'midleft', font)

			
			# show scores button
			scores_button = Button(screen, (WIDTH-225, HEIGHT+25), 'Scores')
			if scores_button.is_clicked():
				game_state = 'scores'
				time.sleep(0.2)
	
	# scores screen
	elif game_state == 'scores':
		screen.blit(bg_image, (0,0))

		# get scores from scores.json
		scoresDict = {}
		with open('scores.json', 'r') as scoresFile:
			scoresDict = load(scoresFile)
		
		# display scores
		if player_1 in scoresDict:
			print_message(f'{player_1}:', (50, 50), 'midleft', font)
			print_message(f'Wins - {scoresDict[player_1]["win"]}', (100, 100), 'midleft', font)
			print_message(f'Losses - {scoresDict[player_1]["lose"]}', (100, 150), 'midleft', font)
			print_message(f'Draws - {scoresDict[player_1]["draw"]}', (100, 200), 'midleft', font)
		if player_2 in scoresDict:
			print_message(f'{player_2}:', (50, 300), 'midleft', font)
			print_message(f'Wins - {scoresDict[player_2]["win"]}', (100, 350), 'midleft', font)
			print_message(f'Losses - {scoresDict[player_2]["lose"]}', (100, 400), 'midleft', font)
			print_message(f'Draws - {scoresDict[player_2]["draw"]}', (100, 450), 'midleft', font)

		# option to play again
		restart_button = Button(screen, (WIDTH//2-100, HEIGHT+25), 'Play again')
		if restart_button.is_clicked():
			game = Game(3,3)
			game_state = 'number_of_players'
			game_over = False
			time.sleep(0.2)

	# update screen
	pygame.display.update()
