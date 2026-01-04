import pygame
from Interfaces.view_interface import ViewInterface

class TrivialPursuitView(ViewInterface):
    def __init__(self, screen, model, orchestrator):
        super().__init__(screen, model, orchestrator)

        # Load once
        self.bg = pygame.image.load("Games/Trivia/Assets/Images/trivial_pursuit.png").convert()

        # Optional: if you want it to match your game_surface size exactly
        # (only do this if your board image is designed for 960x640)
        # self.bg = pygame.transform.smoothscale(self.bg, (960, 640))

    def update(self, dt_ms: int):
        pass

    def render(self):
        # If you are using a fixed game_surface, draw to that:
        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen

        # Draw background at (0,0) for now
        surface.blit(self.bg, (0, 0))


