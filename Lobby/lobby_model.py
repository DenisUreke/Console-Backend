from Enums.game_enum import Game

class LobbyModel:
    def __init__(self):
        self.game_list: Game = Game
        self.current_game_selected = Game.PONG
        

        