# Script for the options screen game state 
import pygame
import sys 

from scripts.settings import *
from states.base_state import BaseState
from scripts.rect_button import RectButton

# options screen class 
class OptionsScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen
        self.fullscreen = False  

    def update(self, events):

        fullscreen_button = RectButton(self.screen, DARK_CYAN, 100, 100, 192, 51, "Fullscreen", WHITE, self.game.font5)
        windowed_button = RectButton(self.screen, DARK_CYAN, 100, 200, 192, 51, "Windowed", WHITE, self.game.font5)
        back_button = RectButton(self.screen, DARK_CYAN, 100, 800, 192, 51, "Back", WHITE, self.game.font5)

        for event in events:
            if fullscreen_button.is_clicked():
                pass
            if windowed_button.is_clicked():
                pass 
            if back_button.is_clicked():
                self.game.state_manager.change_state("title_screen")
        
        self.screen.fill((0, 0, 0))
        
        

        fullscreen_button.draw()
        windowed_button.draw()
        back_button.draw()

