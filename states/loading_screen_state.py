# Script for the loading screen game state 
# Play Button --> Loading Screen --> InGame 
import pygame 

from scripts.settings import * 
from states.base_state import BaseState
from scripts.rect_button import RectButton

# class for the loading screen 
class LoadingScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()

        # Define fonts
        self.font = pygame.font.Font(FONT1, 80)
        self.font1 = pygame.font.Font(FONT2, 80)

        # loading 
        self.progress = 0
    
    # loading bar function, draws it onto the game screen
    def draw_loading_bar(self, progress):

        # draw the progress bar background
        pygame.draw.rect(self.screen, BLACK, (400, 750, 600, 50))
        # draw the progress bar
        pygame.draw.rect(self.screen, WHITE, (410, 755, progress * 5.8, 40))

    

    def update(self, events):


        enter_button = RectButton(self.screen, DARK_CYAN, 1000, 800, 192, 51, "Enter", WHITE, self.game.font5) # the enter game button
        back_button = RectButton(self.screen, DARK_CYAN, 100, 800, 192, 51, "Back", WHITE, self.game.font5) # the back button --> returns to the title screen 

        for event in events:
            if enter_button.is_clicked():
                print("in game")
                self.game.state_manager.change_state("game")
            if back_button.is_clicked():
                self.game.state_manager.change_state("title_screen")

        
        self.screen.fill((0, 0, 0))

        loading_bg = pygame.image.load('data/images/backgrounds/loadingscreen.png').convert_alpha()
        loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))
        self.screen.blit(loading_bg, (0, 0))

        loading_txt = self.font.render('Loading...', True, BLACK)
        self.screen.blit(loading_txt, (530, 500))


        # calculate the width of the loading bar
        self.draw_loading_bar(self.progress)

        if self.progress < 100:
            self.progress += 1
        else:
            # once loading is complete, display the enter button
            enter_button.draw()
            back_button.draw()
            self.progress == False 

        pygame.time.delay(100)
        
        
        pygame.display.update() 
     
