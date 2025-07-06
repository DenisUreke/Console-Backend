from Interfaces.controller_handler_interface import InputHandler

class ButtonPressHandler(InputHandler):
    
    def extract(self, payload):
        return {
            "type": "button_press",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "button": payload.get("button")
        }