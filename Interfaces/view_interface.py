from abc import ABC, abstractmethod

class ViewInterface(ABC):
    def __init__(self, screen, model, orchestrator):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
    
    @abstractmethod
    def update(self, dt_ms: int):
        """Updates the view based on the model state"""
        pass
        
    @abstractmethod
    def render(self):
        """Draws the view based on the model state"""
        pass