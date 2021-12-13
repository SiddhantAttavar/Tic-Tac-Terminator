import pygame, sys, time
from Game import Game
from Buttons import Button, TextButton

WIDTH, HEIGHT = 650, 650

pygame.init()
pygame.display.set_caption('Tic Tac Terminator')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
bg_image = pygame.image.load('assets/background.jpg').convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT+100))
font = pygame.font.Font(None, 40)
font_large = pygame.font.Font(None, 60)

game = Game(3,3)
player = 1
game_state = 'number_of_players'
player_1_name = TextButton(screen, (WIDTH//2, HEIGHT//2))
player_2_name = TextButton(screen, (WIDTH//2, HEIGHT//2))

def print_message(message, pos=(WIDTH // 2, HEIGHT+50), anchor='center', font=font_large):
    text = font.render(message, True, 'darkgreen')
    if anchor == 'center': text_rect = text.get_rect(center = pos)
    elif anchor == 'midleft': text_rect = text.get_rect(midleft = pos)
    screen.blit(text, text_rect)

def draw_board():
    screen.blit(bg_image, (0,0))
    pygame.draw.line(screen, 'black', (WIDTH/3, 0), (WIDTH/3, HEIGHT), 5)
    pygame.draw.line(screen, 'black', (2*(WIDTH/3), 0), (2*(WIDTH/3), HEIGHT), 5)
    pygame.draw.line(screen, 'black', (0, HEIGHT/3), (WIDTH, HEIGHT/3), 5)
    pygame.draw.line(screen, 'black', (0, 2*(HEIGHT/3)), (WIDTH, 2*(HEIGHT/3)), 5)

    for col_ind, col in enumerate(game.board):
        for row_ind, cell in enumerate(col):
            if cell == True:
                surf = pygame.image.load('assets/x.png')
                rect = surf.get_rect(center = (WIDTH//6 + row_ind*(WIDTH//3), HEIGHT//6 + col_ind*(HEIGHT//3)))
                screen.blit(surf, rect)
            elif cell == False:
                surf = pygame.image.load('assets/o.png')
                rect = surf.get_rect(center = (WIDTH//6 + row_ind*(WIDTH//3), HEIGHT//6 + col_ind*(HEIGHT//3)))
                screen.blit(surf, rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == 'number_of_players':
        screen.blit(bg_image, (0,0))
        print_message('How many players?', (WIDTH // 2, HEIGHT // 2 - 100))
        button_1 = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2), '1')
        button_2 = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 100), '2')
        if button_1.is_clicked():
            game_state = 'player_selection'
            botEnabled = True
            time.sleep(0.2)
        elif button_2.is_clicked():
            game_state = 'player_names'
            botEnabled = False
            time.sleep(0.2)
    
    elif game_state == 'player_selection':
        screen.blit(bg_image, (0,0))
        print_message('Play as', (WIDTH // 2, HEIGHT // 2 - 100))
        button_x = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2), 'X')
        button_o = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 100), 'O')
        if button_x.is_clicked():
            game_state = 'player_names'
            player = 1
            time.sleep(0.2)
        elif button_o.is_clicked():
            game_state = 'player_names'
            player = 2
            time.sleep(0.2)
    
    elif game_state == 'player_names':
        screen.blit(bg_image, (0,0))
        print_message('Press ENTER to continue', font=font)
        if botEnabled:
            print_message('Enter your name', (75, HEIGHT // 2), 'midleft', font)
            if player == 1:
                player_1_name.draw(screen, (WIDTH//2, HEIGHT//2 - 25))
                player_1_name.check_active()
                player_1 = player_1_name.get_input()
                player_2 = 'the computer'
            else:
                player_2_name.draw(screen, (WIDTH//2, HEIGHT//2 - 25))
                player_2_name.check_active()
                player_2 = player_2_name.get_input()
                player_1 = 'the computer'
        else:
            print_message('Enter player 1 name', (50, HEIGHT // 2 - 50), 'midleft', font)
            player_1_name.draw(screen, (WIDTH//2, HEIGHT//2 - 75))
            player_1_name.check_active()
            player_1 = player_1_name.get_input()
            print_message('Enter player 2 name', (50, HEIGHT // 2 + 50), 'midleft', font)
            player_2_name.draw(screen, (WIDTH//2, HEIGHT//2 + 25))
            player_2_name.check_active()
            player_2 = player_2_name.get_input()
        
        names = [player_1, player_2]
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if botEnabled:
                game_state = 'bot_difficulty'
            else:
                game_state = 'active'

    elif game_state == 'bot_difficulty':
        screen.blit(bg_image, (0,0))
        print_message('Select difficulty level', (WIDTH // 2, HEIGHT // 2 - 100))
        button_e = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2), 'Easy')
        button_m = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 100), 'Medium')
        button_h = Button(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 200), 'Hard')
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
    
    elif game_state == 'active':
        if not game.gameOver and len(game.remainingCells) > 0:
            draw_board()
            print_message(f'It is {names[not game.turn]}\'s turn', font=font)
            
            if (not botEnabled) or 1 + (not game.turn) == player:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if x < WIDTH/3: col = 0
                    elif x < 2*(WIDTH/3): col = 1
                    else: col = 2
                    if y < HEIGHT/3: row = 0
                    elif y < 2*(HEIGHT/3): row = 1
                    else: row = 2

                    game.makeMove((col, row))
                    
            else:
                move = bot(game)
                game.makeMove(move)
        
        else:
            draw_board()
            if game.gameOver:
                print_message(f'{names[game.turn].capitalize()} won!', (50, HEIGHT+50), 'midleft', font)
            else:
                print_message('It is a draw!', (50, HEIGHT+50), 'midleft', font)
            
            restart_button = Button(screen, (WIDTH-225, HEIGHT+25), 'Play again')
            if restart_button.is_clicked():
                game = Game(3,3)
                game_state = 'number_of_players'
                time.sleep(0.2)

    pygame.display.update()
