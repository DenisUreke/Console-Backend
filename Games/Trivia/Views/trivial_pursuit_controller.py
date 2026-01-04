from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Interfaces.controller_interface import ControllerInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class TrivialPursuitController(ControllerInterface):
    def __init__(self, screen, orchestrator: 'Orchestrator', sound_manager, model: TriviaPursuitModel):
        self.screen = screen
        self.orchestrator = orchestrator
        self.sound_manager = sound_manager
        self.model = model
        
    def start(self):
        '''Initialize game state, variables, assets'''
        for player in self.orchestrator.player_manager.players:
            if player.connected and player.is_in_game:
                self.model.add_player_to_game(
                    player_name=player.name, 
                    player_number=player.player_number, 
                    color=player.color_theme, 
                    websocket_id=player.websocket
                    )
                
        self.model.set_starting_positions()

    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass

    def handle_input(self, event):
        '''Handle input from user'''
        pass

    def update(self):
        '''Update game logic (movement, collisions, scores)'''
        pass

    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
        
        