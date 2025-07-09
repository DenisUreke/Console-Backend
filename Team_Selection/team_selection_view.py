import pygame
from Interfaces.view_interface import ViewInterface
from Team_Selection.team_selectsion_background_img import get_background_image
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class TeamSelectionView(ViewInterface):
    def __init__(self, screen: pygame.Surface, model, orchestrator: 'Orchestrator'):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
        

        self.image_path = get_background_image(orchestrator.state)

        print(f"[DEBUG] Attempting to load background image from: {self.image_path}")
        assert os.path.exists(self.image_path), f"[ERROR] Image file not found: {self.image_path}"

        try:
            self.background_image = pygame.image.load(self.image_path).convert()
        except Exception as e:
            print(f"[ERROR] Failed to load image with pygame: {type(e).__name__} - {e}")
            raise
        self.background = pygame.transform.scale(self.background_image, self.screen.get_size())
        
        pygame.display.set_caption("Team Selection")
        
    def render(self):
        """Draws the view based on the model state"""
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0, 0))