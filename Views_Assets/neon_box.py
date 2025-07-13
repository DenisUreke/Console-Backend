import pygame

class NeonBox:
    def __init__(
        self, 
        screen, 
        object_size=(250, 480), 
        overlay_fill_RGBA=(0, 0, 0, 0), 
        rectangle_colors=((0, 255, 255, 40), (0, 255, 255, 80), (0, 255, 255, 200)),
        rectangle_border_width=(10, 6, 4),
        border_radius=(25, 25, 25),
        position =(0, 0)
        ):
        
        self.screen = screen
        # Default dimensions for the overlay rectangle
        self.object_size = object_size
        # Create a transparent overlay surface
        self.overlay_fill_RGBA = overlay_fill_RGBA
        # Rectangle values
        self.rectangle_colors = rectangle_colors
        # Border width for rectangles
        self.rectangle_border_width = rectangle_border_width
        # Radius for border corners
        self.border_radius = border_radius
        # Position of the overlay
        self.position = position

    def render(self):
        #Size of rectangle x - y
        overlay = pygame.Surface(self.object_size, pygame.SRCALPHA)
        # Fill the overlay
        overlay.fill(self.overlay_fill_RGBA)

        # Draw rectangles values 0 - 255
        pygame.draw.rect(overlay, self.rectangle_colors[0], overlay.get_rect(), width=self.rectangle_border_width[0], border_radius=self.border_radius[0])
        pygame.draw.rect(overlay, self.rectangle_colors[1], overlay.get_rect(), width=self.rectangle_border_width[1], border_radius=self.border_radius[1])
        pygame.draw.rect(overlay, self.rectangle_colors[2], overlay.get_rect(), width=self.rectangle_border_width[2], border_radius=self.border_radius[2])

        self.screen.blit(overlay, self.position)