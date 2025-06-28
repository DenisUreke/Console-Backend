from Joystick_Handlers.joystick_handlers_STANDARD_CONTROLLER import JoystickMoveHandler_STANDARD, JoystickReleaseHandler_STANDARD, ButtonPressHandler_STANDARD
from Enums.controller_enum import ControllerType

class ControllerTranslator():
    def __init__(self):
        self.handlers_by_controller_type = {
            ControllerType.STANDARD_CONTROLLER: {
                "button_press": ButtonPressHandler_STANDARD(),
                "joystick_move": JoystickMoveHandler_STANDARD(),
                "joystick_release": JoystickReleaseHandler_STANDARD()
            }
            # Add more here for each controller
        }
    
    def get_extracted_controller_values(self, controller_type, payload):
        
        input_type = self.get_input_type(payload)
        
        handler = self.handlers_by_controller_type.get(controller_type, {}).get(input_type)
        
        if handler:
            return handler.extract(payload)
        else:
            print(f"[Translator] No handler for input_type '{input_type}' in controller '{controller_type}'")
            return None
        
    
    def get_extracted_data(self, payload, input_type):
        player_name = payload.get("player_name")
        player_number = payload.get("player_number")
        
        if input_type == "joystick_move":
            direction = payload.get("direction")
            distance = payload.get("distance")
            return input_type, player_name, player_number, direction, distance
        elif input_type == "joystick_release":
            released = payload.get("released")
            return input_type, player_name, player_number, released
        elif input_type == "button_press":
            button = payload.get("button")
            return input_type, player_name, player_number, button
        else:
            print("user input_type unknown in function get_extracted_data")
            return None
    
    def get_input_type(self, payload):
        return payload.get("input_type")
    
    def get_angle_to_direction(self, direction) -> str:
        if 75 <= direction <= 105:
            return "up"
        elif 255 <= direction <= 295:
            return "down"
        elif 165 <= direction <= 195:
            return "left"
        elif direction >= 345 or direction <= 15:
            return "right"
        elif 16 <= direction <= 74:
            return "up-right"
        elif 106 <= direction <= 164:
            return "up-left"
        elif 196 <= direction <= 254:
            return "down-left"
        elif 296 <= direction <= 344:
            return "down-right"
        else:
            return "unknown"