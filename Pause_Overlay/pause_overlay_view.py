import pygame

class PauseOverlayView:
    def __init__(self, screen, model, qr_surface=None):
        self.screen = screen
        self.model = model
        self.qr_surface = qr_surface
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

        if self.qr_surface is not None:
            qr_rect = self.qr_surface.get_rect(center=(w//2, h//2))
            self.screen.blit(self.qr_surface, qr_rect)
            y = qr_rect.bottom + 20

        if self.model.url:
            url_surf = self.sub_font.render(self.model.url, True, (255, 255, 255))
            self.screen.blit(url_surf, url_surf.get_rect(center=(w//2, y)))


