# this is the script containing a class that has the function of loading a button
# the button is created using pygame.rect & pygame.elipse 
import pygame

class RectButton:
    def __init__(self, surface, colour, x, y, width, height, text, text_colour, font, hover_colour=None):
        self.surface = surface
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_colour = text_colour
        self.font = font
        self.hover_colour = hover_colour
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        # Check if the mouse is over the button
        is_hovered = self.button_rect.collidepoint(pygame.mouse.get_pos())

        # Draw the rectangular part of the button
        pygame.draw.rect(self.surface, self.colour, self.button_rect, border_radius=25)

        # Draw the semicircles on each end
        left_semicycle_rect = pygame.Rect(self.x, self.y, self.height, self.height)
        right_semicycle_rect = pygame.Rect(self.x + self.width - self.height, self.y, self.height, self.height)

        pygame.draw.ellipse(self.surface, self.colour, left_semicycle_rect)
        pygame.draw.ellipse(self.surface, self.colour, right_semicycle_rect)

        # Draw the glowing outline when hovered or clicked
        if is_hovered:
            pygame.draw.rect(self.surface, (255, 255, 0), self.button_rect, border_radius=25, width=5)  # Yellow glowing outline
        else:
            pygame.draw.rect(self.surface, (255, 255, 255), self.button_rect, border_radius=25, width=5)  # White outline

        button_text = self.font.render(self.text, True, self.text_colour)

        # Adjust font size based on the hover state
        if is_hovered:
            font_size = 40  # Increased font size when hovered
        else:
            font_size = 36

        button_text = pygame.font.Font.render(self.font, self.text, True, self.text_colour)
        button_text = pygame.transform.scale(button_text, (self.width, self.height))

        # Center the text on the button
        text_rect = button_text.get_rect(center=self.button_rect.center)

        self.surface.blit(button_text, text_rect.topleft)

        return self.button_rect
    
    # the click function 
    def is_clicked(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True 
        return False 
