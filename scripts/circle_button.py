"""script for the circle button"""
import pygame 
import math

class CircleButton:
    def __init__(self, surface, colour, x, y, radius, hover_colour=None):
        self.surface = surface
        self.colour = colour 
        self.x = x 
        self.y = y
        self.radius = radius 
        self.hover_colour = hover_colour
        self.button_rect = pygame.Rect(self.x, self.y, self.radius)

    def draw(self):
        # is hovered
        is_hovered = self.button_rect.collidepoint(pygame.mouse.get_pos())

        # draw the perk circle button 
        pygame.draw.circle(self.surface, self.colour, self.button_rect, border_radius=10)

        if is_hovered:
            pygame.draw.circle(self.surface, (255, 255, 0), self.button_rect, border_radius=25, width=5)  # Yellow glowing outline
        else:
            pygame.draw.circle(self.surface, (255, 255, 255), self.button_rect, border_radius=25, width=5)  # White outline

        
        return self.button_rect
    
    # the click function 
    def is_clicked(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True 
        return False 