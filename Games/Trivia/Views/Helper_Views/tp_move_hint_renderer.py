import pygame
import math

from Enums.overlay_enum import OverlayState
from Enums.controller_enum import Controller
from Interfaces.view_interface import ViewInterface


import math
import pygame

class TPMoveHintRenderer:
    """
    Draw animated markers on ring tiles the player can move to.

    - Does NOT compute possible moves.
    - Just renders animated hints for a list of tile indices.
    """

    def __init__(
        self,
        line_width: int = 4,
        base_size: int = 18,
        pulse_amp: float = 0.25,     # how much size grows/shrinks
        pulse_speed_hz: float = 1.6  # pulses per second
    ):
        self.line_width = int(line_width)
        self.base_size = int(base_size)
        self.pulse_amp = float(pulse_amp)
        self.pulse_speed_hz = float(pulse_speed_hz)

        # internal animation clock
        self._t = 0.0

    def update(self, dt_ms: int):
        if dt_ms <= 0:
            return
        self._t += dt_ms / 1000.0

    def render(
        self,
        surface: pygame.Surface,
        ring_tiles,
        possible_indices: list[int],
        camera_x: float,
        camera_y: float,
        color_override=None
    ):
        if not possible_indices:
            return

        # pulse goes 0..1..0
        pulse = (math.sin(self._t * 2.0 * math.pi * self.pulse_speed_hz) + 1.0) * 0.5
        # scale factor e.g. 1.0 ± amp
        scale = 1.0 + (pulse - 0.5) * 2.0 * self.pulse_amp
        size = int(self.base_size * scale)

        # alpha also pulses (nice "breathing" effect)
        alpha = int(120 + pulse * 135)  # 120..255

        for idx in possible_indices:
            if idx < 0 or idx >= len(ring_tiles):
                continue

            tile = ring_tiles[idx]

            sx = int(tile.x - camera_x)
            sy = int(tile.y - camera_y)

            # Choose marker color:
            # - Use override if provided
            # - Else try tile color (hex), fallback white
            if color_override is not None:
                col = color_override
            else:
                col = self._tile_color(tile)

            # draw an alpha-blended X using a temporary surface
            self._draw_pulsing_x(surface, sx, sy, size, col, alpha)

    def _draw_pulsing_x(self, surface, x: int, y: int, size: int, color, alpha: int):
        # render onto a small transparent surface for alpha support
        pad = self.line_width + 2
        w = size * 2 + pad * 2
        h = size * 2 + pad * 2

        temp = pygame.Surface((w, h), pygame.SRCALPHA)
        c = (color[0], color[1], color[2], alpha)

        cx = w // 2
        cy = h // 2

        pygame.draw.line(temp, c, (cx - size, cy - size), (cx + size, cy + size), self.line_width)
        pygame.draw.line(temp, c, (cx - size, cy + size), (cx + size, cy - size), self.line_width)

        # optional outer glow-ish outline (subtle)
        outline = (0, 0, 0, min(140, alpha))
        pygame.draw.line(temp, outline, (cx - size, cy - size), (cx + size, cy + size), 1)
        pygame.draw.line(temp, outline, (cx - size, cy + size), (cx + size, cy - size), 1)

        surface.blit(temp, (x - cx, y - cy))

    def _tile_color(self, tile):
        # If your RingTile has tile.color as WedgeColor or string,
        # try to extract a hex-like string or name.
        raw = getattr(tile, "color", None)
        if raw is None:
            return (255, 255, 255)

        # WedgeColor enum -> its value probably "yellow"/"blue"/etc
        if hasattr(raw, "value"):
            raw = raw.value

        # Simple mapping to neon-ish colors (feel free to swap)
        named = str(raw).lower()
        mapping = {
            "yellow": (255, 240, 90),
            "blue": (80, 180, 255),
            "green": (90, 255, 160),
            "purple": (180, 110, 255),
            "pink": (255, 110, 200),
            "orange": (255, 170, 80),
        }
        return mapping.get(named, (255, 255, 255))
