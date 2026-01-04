
from Enums.overlay_enum import OverlayState


class TriviaOverlayController:
    def __init__(self, model, orchestrator):
        self.model = model
        self.orchestrator = orchestrator

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
                self._handle_dice(event)
            case OverlayState.TRIVIA_QUESTION:
                self._handle_question(event)

    def _handle_dice(self, event):
        # Example: X skips animation / confirms
        if event["type"] == "button_press" and event["button"] == "X":
            # maybe force finish / accept dice result
            self.orchestrator.overlay_state = OverlayState.NONE

    def _handle_question(self, event):
        # Example: joystick selects answer, X confirms
        ...
