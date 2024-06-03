# The script for the Base State Manager

class BaseState:
    def __init__(self, game):
        self.game = game 
  
    
    def enter_state(self):
        pass

    def exit_state(self):
        pass

    def update(self, events):
        self.events = events 
        pass 

    def draw(self, screen):
        pass 