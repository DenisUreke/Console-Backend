import pygame
from Interfaces.view_interface import ViewInterface
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Views_Assets.dice_animation import SpriteDiceRoller  # your file name

class DiceOverlayView(ViewInterface):
    def __init__(self, screen, model: TriviaPursuitModel, orchestrator):
        super().__init__(screen, model, orchestrator)

        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen

        # Center the dice in the viewport
        dice_px = (model.viewport_width // 2 - (16 * 6) // 2,  # tile 16 * scale 6
                   model.viewport_height // 2 - (16 * 6) // 2)

        self.dice = SpriteDiceRoller(screen=surface, pos=dice_px, scale=6, duration_ms=1200)
        self.started = False

    def update(self, dt_ms: int):
        if not self.started:
            self.started = True
            self.model.dice_is_rolling = True
            self.model.dice_result = None
            self.dice.start()

        self.dice.update(dt_ms)

        result = self.dice.get_result()
        if result is not None:
            self.model.dice_is_rolling = False
            self.model.dice_result = result
            # Now controller/orchestrator can close overlay

    def render(self):
        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen

        # Darken background slightly
        dim = pygame.Surface((self.model.viewport_width, self.model.viewport_height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 140))
        surface.blit(dim, (0, 0))

        self.dice.render()
