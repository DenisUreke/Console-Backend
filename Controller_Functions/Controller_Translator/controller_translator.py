from Controller_Functions.Joystick_Handlers.joystick_handlers import (JoystickMoveHandler, JoystickReleaseHandler)
from Controller_Functions.Joystick_Handlers.button_handlers import ButtonPressHandler
from Controller_Functions.Joystick_Handlers.keypad_handlers import KeypadMoveHandler

from Enums.state_enum import State

class ControllerTranslator:
    def __init__(self):
        self.handlers_by_controller_type = {
            State.WELCOME_SCREEN: {
                "keypad_move": KeypadMoveHandler(),
                "button_press": ButtonPressHandler(),
            },
            State.LOBBY: {
                "keypad_move": KeypadMoveHandler(),
                "button_press": ButtonPressHandler(),
            },
            State.TEAM_SELECTION: {
                "button_press": ButtonPressHandler(),
                "keypad_move": KeypadMoveHandler(),
                "joystick_move": JoystickMoveHandler(),
                "joystick_release": JoystickReleaseHandler(),
            },
            State.TRIVIA_LOBBY:{
                "button_press": ButtonPressHandler(),
                "keypad_move": KeypadMoveHandler(),
                "joystick_move": JoystickMoveHandler(),
                "joystick_release": JoystickReleaseHandler(),
            },
            State.TRIVIA: {
                "button_press": ButtonPressHandler(),
            }
        }

    def get_extracted_controller_values(self, state, payload):
        # Get input type
        input_type = self.get_input_type(payload)
        # Get correct handler from factory
        handler = self.handlers_by_controller_type.get(state, {}).get(input_type)

        if handler:
            return handler.extract(payload)
        else:
            print(f"[Translator] No handler for input_type '{input_type}' in controller '{state}'")
            return None

    def get_input_type(self, payload):
        return payload.get("input_type")

