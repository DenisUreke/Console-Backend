from Enums.game_enum import Game
from enum import Enum
from Models.player import Player

class GameType(Enum):
    SINGLE_PLAYER = "single_player"
    MULTI_PLAYER = "multi_player"
    COOPERATIVE = "cooperative"
    VERSUS = "versus"

class GameRulesManager:
    def __init__(self, player_manager):
        self.player_manager = player_manager

        self.game_rules = {
            Game.PONG: {
                "max_players": 4,
                "min_players": 2,
                "game_type": GameType.VERSUS,
            },
            # more rules here laters
        }
    
    def is_game_ready(self, game: Game) -> bool:
        game_rules = self.game_rules.get(game)
        return self.evaluate_game_ready(game_rules)
        
    def evaluate_game_ready(self, game_rules) -> bool:
        count_team_one = sum(1 for p in self.player_manager.players if p.team_selection_position == 0)
        count_team_two = sum(1 for p in self.player_manager.players if p.team_selection_position == 2)
        return (self.evaluate_player_count_in_range(count_team_one, count_team_two, game_rules) and
                self.evaluate_player_distribution(count_team_one, count_team_two, game_rules))
        
    def evaluate_player_count_in_range(self, count_team_one: int, count_team_two: int, game_rules) -> bool:
        total_players = sum([count_team_one, count_team_two])
        return game_rules["min_players"] <= total_players <= game_rules["max_players"]
    
    def evaluate_player_distribution(self, count_team_one: int, count_team_two: int, game_rules) -> bool:
        game_type = game_rules["game_type"]
        
        if game_type == GameType.VERSUS:
            return count_team_one > 0 and count_team_two > 0
        return True 