# this is the script for the animated buttons, mainly used in the pause menu 
import pygame 

class AnimatedButton:
    def __init__(self, x, y, frames):
        self.x = x
        self.y = y 
        self.frames = frames 
        self.current_frame = 0
        self.button_rect = self.frames[0].get_rect(topleft=(x, y))

    
    def draw(self, screen):
        # draw the current frame
        screen.blit(self.frames[self.current_frame], (self.x, self.y))
    
    def update(self):
        # Update the current frame
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0 
    
    def handle_event(self, event):
        # check if the mouse is within the button's area
        mouse_pos = pygame.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.frames[0].get_width() and self.y <= mouse_pos[1] <= self.y + self.frames[0].get_height():
            # if so play the animation 
            self.update()
        else:
            # if not reset the animation
            self.current_frame = 0 
    
    def isclicked(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False 