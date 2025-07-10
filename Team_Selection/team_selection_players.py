from Models.player import Player
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    
class TeamSelectionPlayers:
    def __init__ (self, orchestrator: 'Orchestrator'):
        self.orchestrator = orchestrator
        self.players: list[Player] = orchestrator.player_manager.players


        '''set rules by game enum in orchestrator'''