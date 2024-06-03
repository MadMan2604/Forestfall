# Script to load the button image sprites 
# Using a class called LoadButton
import pygame 

class LoadButton:
    def __init__(self, image, pos):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (373, 72))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos 
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        