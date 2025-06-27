
class Player:
    def __init__(self, websocket, name, player_number, is_leader=False, player_score=0, player_lives = 0, team_selection_position = 1):
        self.websocket = websocket
        self.name = name
        self.player_number = player_number
        self.is_leader = is_leader
        self.player_score = player_score
        self.player_lives = player_lives
        self.team_selection_position = team_selection_position