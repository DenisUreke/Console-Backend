from Controller_Functions.Joystick_Handlers.joystick_handlers_STANDARD_CONTROLLER import (
    JoystickMoveHandler_STANDARD,
    JoystickReleaseHandler_STANDARD,
    ButtonPressHandler_STANDARD,
)
from Controller_Functions.Joystick_Handlers.keypad_handlers_STANDARD_KEYPAD import KeypadMoveHandler_STANDARD

from Enums.js_controller_enum import JsControllerType

class ControllerTranslator:
    def __init__(self):
        self.handlers_by_controller_type = {
            JsControllerType.JS_STANDARD_CONTROLLER: {
                "button_press": ButtonPressHandler_STANDARD(),
                "joystick_move": JoystickMoveHandler_STANDARD(),
                "joystick_release": JoystickReleaseHandler_STANDARD(),
            },
            JsControllerType.KEYPAD_STANDARD_CONTROLLER: {
                "keypad_move": KeypadMoveHandler_STANDARD(),
                "button_press": ButtonPressHandler_STANDARD(),
            }
        }

    def get_extracted_controller_values(self, controller_type, payload):
        # Get input type
        input_type = self.get_input_type(payload)
        # Get correct handler from factory
        handler = self.handlers_by_controller_type.get(controller_type, {}).get(input_type)

        if handler:
            return handler.extract(payload)
        else:
            print(f"[Translator] No handler for input_type '{input_type}' in controller '{controller_type}'")
            return None

    def get_input_type(self, payload):
        return payload.get("input_type")

