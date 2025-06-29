from Interfaces.controller_handler_interface import InputHandler

class JoystickMoveHandler_STANDARD(InputHandler):
    
    def extract(self, payload):
        
        direction = payload.get("direction")
        translated_direction = self.get_angle_to_direction(direction)

        return {
            "type": "joystick_move",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "direction": direction,
            "translated_direction": translated_direction,
            "distance": payload.get("distance")
        }
        
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
        
class JoystickReleaseHandler_STANDARD(InputHandler):
    
    def extract(self, payload):
        return {
            "type": "joystick_release",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "released": payload.get("released")
        }

class ButtonPressHandler_STANDARD(InputHandler):
    
    def extract(self, payload):
        return {
            "type": "button_press",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "button": payload.get("button")
        }
        