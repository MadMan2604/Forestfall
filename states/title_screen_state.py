import pygame 
import sys 
import os 

from scripts.settings import *
from states.base_state import BaseState
from scripts.buttons import LoadButton

class TitleScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()
        #self.animation_frames = []
        #self.frame_rate = frame_rate
        #self.frame_index = 0 
        #self.load_animation_frames() 
        self.cursor = pygame.image.load('data/images/cursor.png').convert_alpha()

        # Define music
        pygame.mixer.init()
        tts_music = 'data/music/Decayed_in_the_Darkness.mp3'
        pygame.mixer.music.load(tts_music)

    def stop_music(self):
        pygame.mixer.music.stop()

    def update(self, events):

        """ define the buttons """
        play_img = BUTTON_PATH + 'titlescreen/play.png' # the play button
        options_img = BUTTON_PATH + 'titlescreen/options.png' # the options button
        information_img = BUTTON_PATH + 'titlescreen/information.png' # the information/keybinds button
        quit_img = BUTTON_PATH + 'titlescreen/quit.png' # the quit button

        """giving the buttons functionality"""
        play_button = LoadButton(play_img, (540, 400)) # play button
        options_button = LoadButton(options_img, (540, 500)) # options button
        information_button = LoadButton(information_img, (540, 600)) # information button
        quit_button = LoadButton(quit_img, (540, 700)) # quit button 


        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    self.game.state_manager.change_state("loading_screen")
                if options_button.rect.collidepoint(event.pos):
                    self.game.state_manager.change_state("options_screen") 
                if information_button.rect.collidepoint(event.pos):
                    self.game.state_manager.change_state("information_screen")
                if quit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit() 
            
            
        # Clear Screen
        self.screen.fill((0, 0, 0))

        """the mouse cursor icon"""
        #x, y = pygame.mouse.get_pos()
        #self.screen.blit(self.cursor, (x, y))
        

        # draw the title screen background
        background_path = BACKGROUND_PATH + 'titlescreen.png'
        background = pygame.image.load(background_path).convert_alpha()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        # draw the title image
        title_path = BACKGROUND_PATH + 'title.png'
        title = pygame.image.load(title_path).convert_alpha()
        title = pygame.transform.scale(title, (WIDTH / 3, HEIGHT / 3))
        self.screen.blit(title, (480, 10))
        
        """draw the buttons onto the screen"""
        play_button.draw(self.screen)
        options_button.draw(self.screen)
        information_button.draw(self.screen)
        quit_button.draw(self.screen)


        pygame.display.flip()
        pygame.display.update()
     