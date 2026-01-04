import math
import pygame

class TPTokenAnimatorRenderer:
    """
    Render + animate TPPlayerToken objects.

    - Animation: moves token.x/y toward token.target_x/target_y at constant speed.
    - Rendering: draws a circle + first letter of player's name.
    - Important: This class does NOT decide targets or game rules.
      Controller/model decide target positions; this class just animates & draws.
    """

    def __init__(self, font: pygame.font.Font, speed_px_per_sec: float = 700.0, radius: int = 14):
        self.font = font
        self.speed_px_per_sec = float(speed_px_per_sec)
        self.radius = int(radius)

    def update_token(self, token, dt_ms: int):
        """
        Animate token.x/y towards token.target_x/target_y using constant speed.
        Sets token.moving True/False accordingly.
        """
        dt = dt_ms / 1000.0
        if dt <= 0:
            return

        dx = token.target_x - token.x
        dy = token.target_y - token.y
        dist = math.hypot(dx, dy)

        # Already at target (or extremely close)
        if dist < 0.01:
            token.x = token.target_x
            token.y = token.target_y
            token.moving = False
            return

        token.moving = True
        step = self.speed_px_per_sec * dt

        # If we can reach target this frame, snap
        if step >= dist:
            token.x = token.target_x
            token.y = token.target_y
            token.moving = False
            return

        # Move toward target with constant speed (normalized direction)
        nx = dx / dist
        ny = dy / dist
        token.x += nx * step
        token.y += ny * step

    def render_player(self, surface: pygame.Surface, player, camera_x: float, camera_y: float):
        """
        Draw the player's token on screen with world->screen transform.
        """
        token = player.player_token

        # world -> screen
        sx = int(token.x - camera_x)
        sy = int(token.y - camera_y)

        # color_theme: your PlayerManager uses COLOR_LIST values.
        # If those are hex strings like "#FF00AA", we parse them.
        color = self._parse_color(player.color_theme)

        # Draw filled circle + outline
        pygame.draw.circle(surface, color, (sx, sy), self.radius)
        pygame.draw.circle(surface, (0, 0, 0), (sx, sy), self.radius, width=2)

        # First letter of name (fallback "?")
        letter = (player.name.strip()[:1].upper() if player.name else "?")

        text_surf = self.font.render(letter, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(sx, sy))
        surface.blit(text_surf, text_rect)

    def _parse_color(self, color_theme: str):
        """
        Accepts:
        - "#RRGGBB"
        - "RRGGBB"
        - or named colors ("red") if pygame supports it (optional)
        Returns an (R,G,B) tuple.
        """
        if not color_theme:
            return (255, 255, 255)

        c = color_theme.strip()

        # Hex
        if c.startswith("#"):
            c = c[1:]

        if len(c) == 6:
            try:
                r = int(c[0:2], 16)
                g = int(c[2:4], 16)
                b = int(c[4:6], 16)
                return (r, g, b)
            except ValueError:
                return (255, 255, 255)

        # Fallback: try pygame.Color for named colors
        try:
            pc = pygame.Color(color_theme)
            return (pc.r, pc.g, pc.b)
        except Exception:
            return (255, 255, 255)
