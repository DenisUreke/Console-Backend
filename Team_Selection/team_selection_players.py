from operator import index
from Models.player import Player
from Team_Selection.team_selection_model import TeamSelectionModel
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    
class TeamSelectionPlayers:
    def __init__ (self, screen: pygame.Surface, model: TeamSelectionModel, orchestrator: 'Orchestrator'):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
        self.players: list[Player] = orchestrator.player_manager.players
        self.center = 420
        self.font_size = 36
        
        '''Create a dictionary to return values so player name is moved depending on team'''
        self.team = {
            0: 100,
            1: 420,
            2: 740
        }
        
        self.reset_team_selection()
        
        #self.font = pygame.font.Font(None, 36)
    
    def render(self):
        if self.model.game_ready:
            self.font_size = 56
        else:
            self.font_size = 36
            
        self.font = pygame.font.Font(None, self.font_size)
        loc_x, loc_y = self.model.position.x, self.model.position.y
        
        for index, player in enumerate(self.players):
            name_surface = self.font.render(player.name, True, (255, 255, 255))
            
            name_rect = name_surface.get_rect()
            name_rect.centerx = loc_x + self.team[player.team_selection_position]
            name_rect.top = loc_y + 100 + index * 40
            
            self.screen.blit(name_surface, name_rect)
            
        '''set rules by game enum in orchestrator'''
        
    def reset_team_selection(self):
        for player in self.players:
            player.team_selection_position = 1
            player.is_in_game = False