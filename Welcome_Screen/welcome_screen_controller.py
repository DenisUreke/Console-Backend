from Welcome_Screen.welcome_screen_model import WelcomeScreenModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    
class WelcomeScreenController:
    def __init__(self, screen, orchestrator: 'Orchestrator', sound_manager, model: WelcomeScreenModel):
        self.screen = screen
        self.orchestrator =orchestrator
        self.sound_manager = sound_manager
        self.model = model
        
    def stop(self): pass
    def update(self): pass
    
    def handle_input(self, translated_payload):
        pass
        
        