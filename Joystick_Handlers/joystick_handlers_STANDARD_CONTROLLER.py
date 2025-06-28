from Interfaces.controller_handler_interface import InputHandler

class JoystickMoveHandler_STANDARD(InputHandler):
    
    def extract(self, payload):
        return {
            "type": "joystick_move",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "direction": payload.get("direction"),
            "distance": payload.get("distance")
        }
        
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
        