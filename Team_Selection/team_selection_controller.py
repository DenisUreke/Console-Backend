from Interfaces.controller_interface import ControllerInterface
from Team_Selection.team_selection_game_rules import GameRulesManager
from Enums.state_enum import State
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    from Team_Selection.team_selection_model import TeamSelectionModel
    from Sound_Manager.sound_manager import SoundManager
    
class TeamSelectionController(ControllerInterface):
    def __init__(self, screen, orchestrator, sound_manager, model):
        self.screen = screen
        self.orchestrator: Orchestrator = orchestrator
        self.sound_manager: SoundManager = sound_manager
        self.model: TeamSelectionModel = model
        self.game_rules_manager: GameRulesManager = GameRulesManager(self.orchestrator.player_manager)


    def start(self):
        '''Initialize game state, variables, assets'''
        pass

    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass

    def handle_input(self, event):
        
        event_type = event.get("type")
        player_number = event.get("player_number")
            
        match event_type: 
            case "button_press":
                button = event.get("button")
                player_number = event.get("player_number")
                self.handle_button_click(button, player_number)
                
            case "keypad_move":
                direction = event.get("direction")
                player_number = event.get("player_number")
                self.handle_keypad_move(direction, player_number)
                    
            case _:
                print(f"Unknown event type: {event_type}")

    def update(self):
        
        if self.model.start_moving:
            direction = self.model.ending_position - self.model.position
            if direction.length() < self.model.speed:
                self.model.position = self.model.ending_position
                self.moving = False
            else:
                self.model.position += direction.normalize() * self.model.speed
    
    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass

    def handle_button_click(self, button, player_number):
        
        if button == 'O':
            self.orchestrator.set_state(State.LOBBY)
            
        if button == "X":
            self.model.update_ending_position()
            self.model.start_moving = True
            # Just for testing need to be changed later <------------------------------------ dont forget
            for player in self.orchestrator.player_manager.players:
                player.is_in_game = True
            self.orchestrator.set_state(State.TRIVIA)    
    
    def handle_keypad_move(self, direction, player_number):
            self.orchestrator.player_manager.set_team_selection_position(player_number, direction)
            if self.game_rules_manager.is_game_ready(self.orchestrator.selected_game):
                self.model.toggle_game_ready(True)
            else:
                self.model.toggle_game_ready(False)
                
        