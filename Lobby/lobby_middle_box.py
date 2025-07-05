import pygame
from Views_Assets.neon_box import NeonBox
from Lobby.lobby_model import LobbyModel

class MiddleBox:
    def __init__ (self, screen, model: LobbyModel):
        self.screen = screen
        self.model = model
        
        self.end_pos = self.model.end_pos
        self.position = self.model.position
        self.speed = 10 ## till controller
        self.moving = self.model.ms_start_moving
        self.font = pygame.font.Font(None, 56)
        pygame.font.init()
         
    def render(self):
        # Create and render the NeonBox first
        game_settings_box = NeonBox(
            self.screen, 
            position=(int(self.position.x), int(self.position.y)), 
            overlay_fill_RGBA=(0, 0, 0, 170), 
            object_size=(480, 620)
        )
        game_settings_box.render()

        # Get the game name string
        game_name = self.model.current_game_selected.value

        # Render the text to a surface
        text_surface = self.font.render(game_name, True, (255, 255, 255))
        text_rect = text_surface.get_rect()

        # Calculate center position
        box_width, box_height = 480, 620
        box_x, box_y = int(self.position.x), int(self.position.y)
        text_rect.center = (box_x + box_width // 2, box_y + 50)

        # Draw the centered text
        self.screen.blit(text_surface, text_rect)