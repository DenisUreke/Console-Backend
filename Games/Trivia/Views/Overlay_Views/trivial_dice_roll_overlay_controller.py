
from Enums.overlay_enum import OverlayState
from Enums.controller_enum import Controller
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
import random
from Interfaces.controller_interface import ControllerInterface
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Games.Trivia.Models.trivia_send_to_front_end import PossibleMove, PossibleMovesData
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator


class TriviaOverlayController(ControllerInterface):
    def __init__(self, screen, orchestrator: 'Orchestrator', sound_manager, model: TriviaPursuitModel):
        self.screen = screen
        self.orchestrator = orchestrator
        self.sound_manager = sound_manager
        self.model = model

    def handle_input(self, event):
        # If no overlay, ignore
        if self.orchestrator.overlay_state == OverlayState.NONE:
            return

        # Global overlay controls (works everywhere)
        if event["type"] == "button_press" and event["button"] == "O":
            self.orchestrator.overlay_state = OverlayState.NONE
            return

        # Overlay-specific controls
        match self.orchestrator.overlay_state:
            case OverlayState.TRIVIA_DICE_ROLL:
                if self.model.dice_phase == DiceOverlayPhase.PROMPT:
                    self.handle_start_roll(event)
                if self.model.dice_phase == DiceOverlayPhase.ROLLING:
                    pass
                if self.model.dice_phase == DiceOverlayPhase.RESULT:
                    self._handle_dice(event)
                    
            case OverlayState.TRIVIA_QUESTION:
                self._handle_question(event)

    def handle_start_roll(self, event):
        self.model.dice_value = random.randint(1, 6) # Simulate dice roll
        self.model.dice_phase = DiceOverlayPhase.ROLLING

    def _handle_dice(self, event):
        self.conclude_dice_roll()
        self.model.phase = TPPhase.CHOOSE_MOVE
        self.orchestrator.overlay_state = OverlayState.NONE
        self.model.dice_phase = DiceOverlayPhase.PROMPT

    def _handle_question(self, event):
        # Example: joystick selects answer, X confirms
        pass
    
    def start(self):
        '''Initialize game state, variables, assets'''
        pass
        
    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass
    def update(self, dt_ms: int):
        '''Update game logic (movement, collisions, scores)'''
        pass
    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
    def conclude_dice_roll(self):
        self.model.possible_move_indices = self.model.get_possible_moves(self.model.dice_value)
        possible_moves_data: PossibleMovesData = self.model.build_possible_moves_data(self.model.dice_value, self.model.possible_move_indices)
        package = self.orchestrator.message_parser.trivia_message_parser.get_possible_moves_message(possible_moves_data)
        self.orchestrator.broadcasting_manager.broadcast_to_specific_client(self.model.get_current_player().websocket_id, package)
        self.model.dice_value = None
        
        '''Handle end of dice roll, move to next phase'''
        ...
