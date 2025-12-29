from Interfaces.controller_handler_interface import InputHandler

class ButtonPressHandler(InputHandler):

    def extract(self, payload):
        button = payload.get("button")

        # Special-case: pause toggle (keeps frontend simple for now)
        if isinstance(button, str) and button.upper() == "PAUSE":
            return {
                "type": "pause_toggle",
                "player_name": payload.get("player_name"),
                "player_number": payload.get("player_number"),
            }

        return {
            "type": "button_press",
            "player_name": payload.get("player_name"),
            "player_number": payload.get("player_number"),
            "button": button
        }
