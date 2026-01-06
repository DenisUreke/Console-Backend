import json
from Enums.controller_enum import Controller
from Message_Parser.trivia_message_parser import TriviaMessageParser

class MessageParser():
    def __init__(self):
        self.trivia_message_parser = TriviaMessageParser()
        
    def get_parsed_player_list(self, player_manager):
        player_list = []
        for player in player_manager.players:
            player_list.append({
                "name": player.name,
                "player_number": player.player_number,
                "is_leader": player.is_leader,
                "player_score": player.player_score,
                "player_lives": player.player_lives,
                "team_selection_position": player.team_selection_position,
                "is_in_game": player.is_in_game,
                "color_theme": player.color_theme
            })
        message = {
            "type": "player_list_update",
            "data": {
                "players": player_list,
                "player_count": len(player_manager.players)
            }
        }

        return json.dumps(message)
    
    def get_parsed_change_controller(self, controller_type: Controller, player_number = "all"):
        
        message = {
            "type": "controller_change",
            "data": {
                "player_number": player_number,
                "controller_type": controller_type.name
            }
        }
        
        return json.dumps(message)
    
    def get_parsed_session_token(self, session_token: str):
        message = {
            "type": "session_token",
            "data": {
                "session_token": session_token
            }
        }
        
        return json.dumps(message)
    
    def get_parsed_trivia_questions(self, questions):
        return self.trivia_message_parser.get_parsed_trivia_questions(questions)
    
    