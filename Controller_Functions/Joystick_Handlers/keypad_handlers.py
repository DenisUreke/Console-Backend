from Interfaces.controller_handler_interface import InputHandler

class KeypadMoveHandler(InputHandler):
    
    def extract(self, payload):
        return {
            "type": "keypad_move",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "direction": payload.get("direction")
        }