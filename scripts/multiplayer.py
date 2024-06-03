# script for the multiplayer functionality 
# online connectivity 
import pygame 
import sys 

from entities import Player

class Multiplayer:
    def __init__(self, game, player, pos, entity):
        super().__init__(game)
        self.player = player 
        player = Player
        self.pos = Player.rect.get_pos()
        self.entity = entity 
        self.pos = pos 
    
    def join_game(self, multi_player):
        self.multiplayer = join_game(multi_player)