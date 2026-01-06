import pygame
from Interfaces.view_interface import ViewInterface
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Views_Assets.dice_animation import SpriteDiceRoller  # your file name
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class DiceOverlayView(ViewInterface):
    def __init__(self, screen, model: TriviaPursuitModel, orchestrator: 'Orchestrator'):
        super().__init__(screen, model, orchestrator)

        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen
        self.font = pygame.font.Font(None, 40)

        # Center the dice in the viewport
        dice_px = (model.viewport_width // 2 - (16 * 6) // 2,  # tile 16 * scale 6
                   model.viewport_height // 2 - (16 * 6) // 2)

        self.dice = SpriteDiceRoller(screen=surface, pos=dice_px, scale=6, duration_ms=1200)
        self.started = False

    def update(self, dt_ms: int):
        # 1) Waiting for user input (controller should switch phase to ROLLING)
        if self.model.dice_phase == DiceOverlayPhase.PROMPT:
            return

        # 2) Start rolling exactly once when phase becomes ROLLING
        if self.model.dice_phase == DiceOverlayPhase.ROLLING:
            if not self.started:
                # dice_value must be set by controller before switching to ROLLING
                self.model.dice_is_rolling = True
                self.model.dice_result = None
                self.dice.start(forced_result=self.model.dice_value)
                self.started = True

            self.dice.update(dt_ms)

            result = self.dice.get_result()
            
            if result is not None:
                self.model.dice_is_rolling = False
                self.model.dice_result = result
                self.model.dice_phase = DiceOverlayPhase.RESULT
            return

        # 3) RESULT phase: do nothing here (controller can close overlay on button press) <---- brain is not braining
        if self.model.dice_phase == DiceOverlayPhase.RESULT:
            return


    def render(self):
        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen

        # Dim background
        dim = pygame.Surface((self.model.viewport_width, self.model.viewport_height), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 140))
        surface.blit(dim, (0, 0))

        if self.model.dice_phase == DiceOverlayPhase.PROMPT:
            text = self.font.render("Press X to roll", True, (255, 255, 255))
            rect = text.get_rect(center=(self.model.viewport_width // 2, self.model.viewport_height // 2))
            surface.blit(text, rect)
            return

        # ROLLING or RESULT: draw dice animation (and it will show final face in RESULT too)
        self.dice.render()

        if self.model.dice_phase == DiceOverlayPhase.RESULT:
            text = self.font.render("Press X to continue", True, (255, 255, 255))
            rect = text.get_rect(center=(self.model.viewport_width // 2, (self.model.viewport_height // 2) + 120))
            surface.blit(text, rect)

