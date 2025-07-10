import pygame
from Enums.image_path_enum import ImagePath
from Interfaces.view_interface import ViewInterface
from Team_Selection.team_selection_box import TeamSelectionBox
from Team_Selection.team_selection_players import TeamSelectionPlayers
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class TeamSelectionView(ViewInterface):
    def __init__(self, screen: pygame.Surface, model, orchestrator: 'Orchestrator'):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
        
        self.box = TeamSelectionBox(self.screen, self.model)
        self.players = TeamSelectionPlayers(self.screen, self.model, orchestrator)
        
        # Load background image
        image_path = ImagePath.get_image_path(self.orchestrator.state)
        original_bg = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(original_bg, self.screen.get_size())
        
    def render(self):
        
        self.screen.blit(self.background, (0, 0))
        
        self.box.render()
        self.players.render()