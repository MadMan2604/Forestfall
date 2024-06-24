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

    def restart_state(self, state_name=None):
        # restarts the given state or the current state if no state name is there
        if state_name:
            # restart a specific state by name 
            if state_name in self.states:
                self.states[state_name].exit_state()
                # reinitialize the state (assuming the state class has an initialization method)
                self.states[state_name].__init__(self.game)
                self.change_state(state_name)
            else:
                # Restart the current state
                if self.current_state:
                    current_state_name = [name for name, state in self.states.items() if state == self.current_state][0]
                    self.current_state.exit_state()
                    self.current_state.__init__(self.game)
                    self.change_state(current_state_name)



