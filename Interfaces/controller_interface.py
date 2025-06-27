from abc import ABC, abstractmethod

class ControllerInterface(ABC):
    def __init__(self, screen, orchestrator, sound_manager):
        self.screen = screen
        self.orchestrator = orchestrator
        self.sound_manager = sound_manager
        
@abstractmethod
def start(self):
    '''Initialize game state, variables, assets'''
    pass

@abstractmethod
def stop(self):
    '''Clean up resources, stop threads/timers'''
    pass

@abstractmethod
def handle_input(self, event):
    '''Handle input from user'''
    pass

@abstractmethod
def update(self):
    '''Update game logic (movement, collisions, scores)'''
    pass
    
@abstractmethod
def handle_fx(self, event_name: str):
    '''Play sounds associtiated with game events'''
    pass
