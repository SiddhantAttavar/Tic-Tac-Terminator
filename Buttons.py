'''This file contains classes for the buttons used in the GUI:
 - Button: Standard button
 - TextButton: Button that accepts text input
'''

#import packages
import pygame

class Button:
    '''This class creates a button object

    Attributes
    ----------
    rect : pygame.Rect
        The rectangle of the button
    text : pygame.Surface
        The text of the button
    text_rect : pygame.Rect
        The rectangle of the text
    
    Methods
    -------
    __init__() -> None
        Initializes the button object
    is_clicked() -> bool
        Returns True if the button is clicked
    '''

    def __init__(self, screen, pos, message):
        '''Initializes the button object

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the button on
        pos : tuple
            The position of the topleft corner of the button
        message : str
            The text of the button
        '''
        
        #create the button components
        font = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(pos, (200, 50))
        self.text = font.render(message, True, 'white')
        self.text_rect = self.text.get_rect(center=self.rect.center)

        #draw the rectangle and text on the screen
        pygame.draw.rect(screen, 'red', self.rect, border_radius=8)
        screen.blit(self.text, self.text_rect)
    
    def is_clicked(self):
        '''Check if the button is clicked
        
        Returns
        -------
        bool
            True if the button is clicked
        '''

        #get mouse position
        mouse_pos = pygame.mouse.get_pos()

        #check if mouse is inside the button and if it is pressed
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


class TextButton(Button):
    '''This class creates a button object that accepts text input
    
    Attributes
    ----------
    input_text : str
        The text that is inputted by the user
    is_active : bool
        True if the button is currently selected
    rect : pygame.Rect
        The rectangle of the button
    text : pygame.Surface
        The text displayed on the button
    text_rect : pygame.Rect
        The rectangle of the text
    
    Methods
    -------
    __init__() -> None
        Initializes the button object
    draw() -> None
        Draws the button on the screen
    check_active() -> None
        Checks if the button is currently selected
    get_input() -> str
        Gets input from the user and returns the inputted text
    '''
    
    def __init__(self, screen, pos):
        '''Initializes the button object
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the button on
        pos : tuple
            The position of the topleft corner of the button
        '''

        #initialize values
        super().__init__(screen, pos, '')
        self.input_text = ''
        self.is_active = False
    
    def draw(self, screen, pos):
        '''Draws the button on the screen
        
        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the button on
        pos : tuple
            The position of the topleft corner of the button
        '''

        #create button components
        message = self.input_text
        font = pygame.font.Font(None, 30)
        self.rect = pygame.Rect(pos, (300, 50))
        self.text = font.render(message, True, 'white')
        self.text_rect = self.text.get_rect(center=self.rect.center)

        #draw the rectangle and text on the screen
        if self.is_active: pygame.draw.rect(screen, 'blue', self.rect)
        else: pygame.draw.rect(screen, 'red', self.rect)
        screen.blit(self.text, self.text_rect)

    def check_active(self):
        '''Checks if the button is currently selected'''
        
        #check if mouse is clicked inside the button or outside of it
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.is_active = True
            else:
                self.is_active = False
    
    def get_input(self):
        '''Gets input from the user and returns the inputted text'''

        #check if the button is active
        if self.is_active:
            #event loop which checks for keypresses
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        
        return self.input_text.strip()
