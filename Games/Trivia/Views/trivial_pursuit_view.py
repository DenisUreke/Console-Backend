import pygame
from Interfaces.view_interface import ViewInterface
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Games.Trivia.Enums_Trivia.trivia_camera_mode_enum import TriviaCameraModeEnum
from Games.Trivia.Models.tpp_player_model import TPPlayer
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
from Games.Trivia.Models.tpp_player_model import TPPlayerToken
from Games.Trivia.Views.Helper_Views.tp_token_animator_renderer import TPTokenAnimatorRenderer
from Games.Trivia.Views.Helper_Views.tp_move_hint_renderer import TPMoveHintRenderer
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator


class TrivialPursuitView(ViewInterface):
    def __init__(self, screen, model: TriviaPursuitModel, orchestrator: 'Orchestrator'):
        super().__init__(screen, model, orchestrator)

        # Load once
        self.bg = pygame.image.load("Games/Trivia/Assets/Images/trivial_pursuit.png").convert()
        self.token_font = pygame.font.Font(None, 48)  # default font, size 20
        self.token_renderer = TPTokenAnimatorRenderer(font=self.token_font, speed_px_per_sec=700, radius=28)
        self.hint_renderer = TPMoveHintRenderer()


        # Optional: if you want it to match your game_surface size exactly
        # (only do this if your board image is designed for 960x640)
        # self.bg = pygame.transform.smoothscale(self.bg, (960, 640))

    def update(self, dt_ms: int):
        # No players / no active turn -> nothing to follow
        if not self.model.players or self.model.current_player_turn is None:
            return

        # Find active player
        active_player = next(
            (p for p in self.model.players if p.player_number == self.model.current_player_turn),
            None
        )
        if not active_player:
            return

        # Convert dt to seconds
        dt = dt_ms / 1000.0
        max_delta = self.model.camera_speed_px_per_sec * dt

        # Helper: clamp camera target to world bounds
        max_x = self.model.world_width - self.model.viewport_width
        max_y = self.model.world_height - self.model.viewport_height

        # Desired target = center camera on active token
        px = active_player.player_token.x
        py = active_player.player_token.y

        desired_tx = px - (self.model.viewport_width / 2)
        desired_ty = py - (self.model.viewport_height / 2)

        desired_tx = self._clamp(desired_tx, 0, max_x)
        desired_ty = self._clamp(desired_ty, 0, max_y)

        # FOLLOW: camera target updates continuously
        if self.model.camera_mode == TriviaCameraModeEnum.FOLLOW:
            self.model.camera_target_x = desired_tx
            self.model.camera_target_y = desired_ty

        # Move camera toward current target (FOLLOW and TRANSITION both use this)
        self.model.camera_x = self._move_towards(self.model.camera_x, self.model.camera_target_x, max_delta)
        self.model.camera_y = self._move_towards(self.model.camera_y, self.model.camera_target_y, max_delta)

        # If we're transitioning and arrived -> switch to FOLLOW
        if self.model.camera_mode == TriviaCameraModeEnum.TRANSITION:
            if self.model.camera_x == self.model.camera_target_x and self.model.camera_y == self.model.camera_target_y:
                self.model.camera_mode = TriviaCameraModeEnum.FOLLOW
        
        # update move hint animator
        self.hint_renderer.update(dt_ms)
                
        # Update all player tokens
        for p in self.model.players:
            self.token_renderer.update_token(p.player_token, dt_ms)



    def render(self):
        # If you are using a fixed game_surface, draw to that:
        surface = self.orchestrator.game_surface if hasattr(self.orchestrator, "game_surface") else self.screen

        # treat the background image as asprite sheet and draw a portion based on camera position
        cx = max(
            0,
            min(int(self.model.camera_x),
                self.model.world_width - self.model.viewport_width)
        )
        cy = max(
            0,
            min(int(self.model.camera_y),
                self.model.world_height - self.model.viewport_height)
        )

        camera_rect = pygame.Rect(
            cx,
            cy,
            self.model.viewport_width,
            self.model.viewport_height
        )
        surface.blit(self.bg, (0, 0), camera_rect)
        
        # Draw move hints if in CHOOSE_MOVE phase
        if self.model.phase == TPPhase.CHOOSE_MOVE:
            self.hint_renderer.render(
                surface,
                self.model.ring_tiles,
                self.model.possible_move_indices,
                self.model.camera_x,
                self.model.camera_y
            )
        
        # Draw all player tokens
        for p in self.model.players:
            self.token_renderer.render_player(surface, p, cx, cy)

        
    ####### Helper functions #######
    
    # We use this for camera bounds so the camera never samples outside the board image.
    def _clamp(self, v: float, lo: float, hi: float) -> float:
        return max(lo, min(v, hi))
    
    # We use this for smooth camera transitions (and can reuse it for token movement too).
    def _move_towards(self, current: float, target: float, max_delta: float) -> float:
        if abs(target - current) <= max_delta:
            return target
        return current + max_delta if target > current else current - max_delta





