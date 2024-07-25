"""script for the circle button"""
import pygame 
import math

class CircleButton:
    def __init__(self, surface, colour, x, y, radius, icon_path, hover_colour=None):
        self.surface = surface
        self.colour = colour 
        self.x = x 
        self.y = y
        self.radius = radius 
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (radius * 2, radius *2)) # scale the icon to fit the center of the circle  
        self.hover_colour = hover_colour if hover_colour else colour

    def draw(self):
        # get the mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # calculate the distance from the center of the button to the mouse position
        distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5

        # determine if the button is hovered
        is_hovered = distance <= self.radius

        # draw the button with the hover effect
        button_colour = self.hover_colour if is_hovered else self.colour
        pygame.draw.circle(self.surface, button_colour, (self.x, self.y), self.radius, width=5)

        # draw the icon centerd on the button
        icon_rect = self.icon.get_rect(center=(self.x, self.y))
        self.surface.blit(self.icon, icon_rect)
    
    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
                if distance <= self.radius:
                    return True
            return False 
   

   