import pygame 
import sys 
import os 

from scripts.settings import * 
from states.base_state import BaseState
from scripts.rect_button import RectButton

# script for the pause menu, that is a game state that activates when the game is paused and nothing is updating at the current period in time.
class PauseMenu(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()

    def update(self, events):

        resume_button = RectButton(self.screen, DARK_CYAN, 100, 100, 192, 51, "Resume", WHITE, self.game.font5)
        restart_button = RectButton(self.screen, DARK_CYAN, 100, 250, 192, 51, "Restart", WHITE, self.game.font5)
        main_menu_button = RectButton(self.screen, DARK_CYAN, 100, 450, 192, 51, "Main Menu", WHITE, self.game.font5)
        quit_button = RectButton(self.screen, DARK_CYAN, 100, 600, 192, 51, "Quit", WHITE, self.game.font5)

        for event in events:
            if event.type == pygame.quit():
                pygame.quit()
                sys.exit()

            if restart_button.is_clicked():
                self.game.state_manager.exit_state()
            if resume_button.is_clicked():
                self.game.state_manager.change_state("game")
            if main_menu_button.is_clicked():
                self.game.state_manager.change_state("title_screen")
            if quit_button.is_clicked():
                pygame.quit()
                sys.exit()
        

        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(FPS)
        