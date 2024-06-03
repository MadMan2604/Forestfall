# The main script that loads the game 
import pygame 

from game import Game
from scripts.settings import *

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init() 
    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode((screen_size))
    game = Game(screen)
    game.run() 
    