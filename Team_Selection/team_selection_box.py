import pygame
from Views_Assets.neon_box import NeonBox
from Team_Selection.team_selection_model import TeamSelectionModel

class TeamSelectionBox:
    def __init__(self, screen, model: TeamSelectionModel):
        self.screen = screen
        self.model = model
        self.screen_width = 1280
        self.screen_height = 720
        
        self.starting_position = pygame.Vector2(self.screen_width//2 -420, self.screen_height//2 -1000)
        self.ending_position = pygame.Vector2(self.screen_width//2 -420, self.screen_height//2-325)
        
        self.position = self.starting_position.copy()
        self.speed = 10
        self.is_moving = True
        
        self.box = NeonBox(
            self.screen,
            position= (self.position.x, self.position.y),
            object_size= (840, 650),
            overlay_fill_RGBA=(0,0,0,170)
        )
    def render(self):
        pass