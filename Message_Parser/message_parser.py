import json

class MessageParser():
    def __init__(self):
        pass
        
    def get_parsed_player_list(self, player_manager):
        player_list = []
        for player in player_manager.players:
            player_list.append({
                "name": player.name,
                "player_number": player.player_number,
                "is_leader": player.is_leader,
                "player_score": player.player_score,
                "player_lives": player.player_lives
            })
        message = {
            "type": "player_list_update",
            "data": {
                "players": player_list,
                "player_count": len(player_manager.players)
            }
        }
        # Convert to JSON
        message_json = json.dumps(message)
        
        return message_json
        