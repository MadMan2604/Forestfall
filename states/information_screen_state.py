# The script for the information screen
# This game state shows the keybinds for the game
# There is a back button to return to the title screen 
# There is a keybinds button to navigate the player to a screen showing written descriptions of the keys used to play the game

import pygame 
import os
import sys

from scripts.settings import * 
from states.base_state import BaseState
from scripts.rect_button import RectButton

# information screen class
class InformationScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()
    
    # the update funciton that runs the game state via the state manager
    def update(self, events):

        # buttons 
        ## back button construction
        back_button = RectButton(self.screen, DARK_CYAN, 100, 800, 192, 51, "Back", WHITE, self.game.font5)


        for event in events:
            if back_button.is_clicked():
                self.game.state_manager.change_state("title_screen")
                
        

        self.screen.fill((0, 0, 0))

        information_bg = pygame.image.load(BACKGROUND_PATH + 'informationscreen.png')
        information_bg = pygame.transform.scale(information_bg, (WIDTH, HEIGHT))

        self.screen.blit(information_bg, (0, 0))

       
        # keyboard layout img
        keyboard = pygame.image.load(BUTTON_PATH + 'informationscreen/keys.png').convert_alpha()
        self.screen.blit(keyboard, (120, 200))

        back_button.draw()

        

        pygame.display.update() 
        pygame.display.flip()
        self.clock.tick(FPS)


  