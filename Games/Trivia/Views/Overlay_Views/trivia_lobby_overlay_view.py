import pygame
from Interfaces.view_interface import ViewInterface
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Views_Assets.dice_animation import SpriteDiceRoller  # your file name
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator
    
class TriviaLobbyOverlayView(ViewInterface):
    def __init__(self, screen, model: TriviaPursuitModel, orchestrator: 'Orchestrator'):
        super().__init__(screen, model, orchestrator)

        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen
        self.font = pygame.font.Font(None, 40)

    def update(self, dt_ms: int):
        pass


    def render(self):
        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen
        # Dim background
        dim = pygame.Surface((self.model.viewport_width, self.model.viewport_height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 140))
        surface.blit(dim, (0, 0))
        
        text = self.font.render("Click button to start", True, (255, 255, 255))
        rect = text.get_rect(center=(self.model.viewport_width // 2, self.model.viewport_height // 2))
        surface.blit(text, rect)