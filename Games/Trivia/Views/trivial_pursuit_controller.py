from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Interfaces.controller_interface import ControllerInterface
from Enums.overlay_enum import OverlayState
from Enums.controller_enum import Controller
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
from Enums.state_enum import State
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
        self.model.set_starting_player()
        self.orchestrator.set_controller(Controller.TRIVIA)
        self.orchestrator.overlay_state = OverlayState.NONE

    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass

    def handle_input(self, event):
        '''Handle input from user'''
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
        '''Update game logic (movement, collisions, scores)'''
        pass

    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
    
    def handle_button_click(self, button, player_number):
        
        match self.orchestrator.state:
            
          case State.TRIVIA_LOBBY:
            self.start()
            self.orchestrator.state = State.TRIVIA
            return
            
          case State.TRIVIA:
            match self.model.phase:
                case TPPhase.AWAIT_ROLL:
                    if button == 'X':
                        self.orchestrator.set_overlay_state(OverlayState.TRIVIA_DICE_ROLL)
                        return
        
        if self.orchestrator.state == State.TRIVIA_LOBBY:
            self.start()
            self.orchestrator.state = State.TRIVIA
            return
            
        if button == 'X':
            #self.model.set_next_player_turn()
            self.model.dice_phase = DiceOverlayPhase.PROMPT
            self.model.dice_value = None
            self.orchestrator.overlay_state = OverlayState.TRIVIA_DICE_ROLL

            
            '''print("turn:", self.model.current_player_turn,
            "mode:", self.model.camera_mode,
            "cam:", self.model.camera_x, self.model.camera_y,
            "target:", self.model.camera_target_x, self.model.camera_target_y)'''
    
    def handle_keypad_move(self, direction, player_number):
        pass
        
        