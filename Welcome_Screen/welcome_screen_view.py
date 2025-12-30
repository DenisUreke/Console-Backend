from Welcome_Screen.welcome_screen_model import WelcomeScreenModel
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class WelcomeScreenView:
    def __init__ (self, screen, model, orchestrator: 'Orchestrator'):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
        self.title_font = pygame.font.SysFont(None, 96)
        self.sub_font = pygame.font.SysFont(None, 28)
        
    def render(self):
        w, h = self.screen.get_size()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(w//2, 90)))

        y = h//2 + 150  # fallback if no QR