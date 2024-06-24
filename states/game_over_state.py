import pygame
import sys

from states.base_state import BaseState
from scripts.settings import * 
from scripts.rect_button import RectButton

class Game_Over(BaseState):
    def __init__(self, game):
        super().__init__(game) # super class the game itself 
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()

        pygame.mixer.init() # initialise the muusic

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            