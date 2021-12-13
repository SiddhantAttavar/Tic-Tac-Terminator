from sys import byteorder
import pygame

class Button:
    def __init__(self, screen, pos, message):
        font = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(pos, (200, 50))
        self.text = font.render(message, True, 'white')
        self.text_rect = self.text.get_rect(center=self.rect.center)
        pygame.draw.rect(screen, 'red', self.rect, border_radius=8)
        screen.blit(self.text, self.text_rect)
    
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

class TextButton(Button):
    def __init__(self, screen, pos):
        super().__init__(screen, pos, '')
        self.input_text = ''
        self.is_active = False
    
    def draw(self, screen, pos):
        self.message = self.input_text
        font = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(pos, (300, 50))
        self.text = font.render(self.message, True, 'white')
        self.text_rect = self.text.get_rect(center=self.rect.center)
        if self.is_active: pygame.draw.rect(screen, 'yellow', self.rect)
        else: pygame.draw.rect(screen, 'red', self.rect)
        screen.blit(self.text, self.text_rect)

    def check_active(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.is_active = True
            else:
                self.is_active = False
    
    def get_input(self):
        if self.is_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        return self.input_text.strip()