from abc import ABC, abstractmethod

class ViewInterface(ABC):
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        
    @abstractmethod
    def render(self):
        """Draws the view based on the model state"""
        pass