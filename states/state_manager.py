# This is the script for the game state machine 
class StateManager:
    def __init__(self, game):
        self.game = game 
        self.states = {}
        self.current_state = None 
        

    def add_state(self, state_name, state):
        # Adds a new state to the state manager.
        self.states[state_name] = state

    def change_state(self, state_name):
        # Changes the current state of the game to the given state name.
        if self.current_state:
            self.current_state.exit_state()
        self.current_state = self.states.get(state_name)
        if self.current_state:
            self.current_state.enter_state()

    def update(self, events):
        # Updates the current state.
        if self.current_state:
            self.current_state.update(events)

    def draw(self, screen):
        # Draws the current state.
        if self.current_state:
            self.current_state.draw(screen)

    def exit_state(self):
        # Exits the current state.
        if self.current_state:
            self.current_state.exit_state()
            self.current_state = None


