
from Enums.overlay_enum import OverlayState
import random
from Interfaces.controller_interface import ControllerInterface
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase


class TriviaOverlayController(ControllerInterface):
    def __init__(self, screen, orchestrator, sound_manager, model):
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
        self.orchestrator.overlay_state = OverlayState.NONE

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
        ...
