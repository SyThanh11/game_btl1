class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state
        
    def getState(self):
        return self.current_state
    
    def setState(self, new_state):
        self.current_state = new_state