# script for the portals 
import pygame 
import math
import random 
import os 
import pygame.mixer 

from scripts.particle import Particle
from scripts.settings import *
from scripts.spark import Spark

class PortalEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
            
        self.last_movement = movement
        
        # Commented out the gravity effect
        # self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        # Commented out the ground collision effect
        # if self.collisions['down'] or self.collisions['up']:
        #     self.velocity[1] = 0
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

# the class for the portal
## if the player dashes into the portal colliding with it, the level changes to the alternate level

# this is the portal class using the particles class as reference 
class Portals(PortalEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'portal', pos, size)

        

    def update(self, tilemap, movement=(0, 0)):

        keys = pygame.key.get_pressed()
        if self.rect().colliderect(self.game.player.rect()):
            self.game.screen.blit(self.game.interaction_icon, (self.game.player.pos[0], self.game.player.pos[1]))
            if keys[pygame.K_e] == True:
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                self.game.load_level(self.game.alt_level)
        
        
        
            
        super().update(tilemap, movement=movement)
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

         

