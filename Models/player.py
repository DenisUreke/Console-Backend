
import time

class Player:
    def __init__(self, 
                 websocket, 
                 name, 
                 player_number, 
                 is_leader=False, player_score=0, 
                 player_lives = 0, 
                 team_selection_position = 1, 
                 is_in_game = False, 
                 color_theme = "",
                 session_token: str = "",
                 connected = True,
                 last_seen = time.time()
                 ):
        
        self.websocket = websocket
        self.name = name
        self.player_number = player_number
        self.is_leader = is_leader
        self.player_score = player_score
        self.player_lives = player_lives
        self.team_selection_position = team_selection_position
        self.is_in_game = is_in_game
        self.color_theme = color_theme
        self.session_token = session_token
        self.connected = connected
        self.last_seen = last_seen