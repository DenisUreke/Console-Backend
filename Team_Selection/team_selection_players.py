from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    
class TeamSelectionPlayers:
    def __init__ (self, orchestrator: 'Orchestrator'):
        self.orchestrator = orchestrator
        self.players: dict = orchestrator.player_manager.game_players_dict
        
        '''set rules by game enum in orchestrator'''