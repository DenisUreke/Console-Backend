import pygame

class SimpleRectangle:
    def __init__(
        self,
        screen,
        height=100,
        width=100,
        border_width=0,
        border_radius=0,
        border_color=(0, 0, 0),   # doesn't matter if border_width = 0
        color_fill=(255, 255, 255),  # white fill
        position=(0, 0)
    ):
        self.screen = screen
        self.height = height
        self.width = width
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color
        self.color_fill = color_fill
        self.position = position
        
    def render(self):
        rect = pygame.Rect(self.position, (self.width, self.height))
        pygame.draw.rect(
            self.screen,
            self.color_fill,
            rect,
            border_radius=self.border_radius
        )

        if self.border_width > 0:
            pygame.draw.rect(
                self.screen,
                self.border_color,
                rect,
                width=self.border_width,
                border_radius=self.border_radius
            )
        
        