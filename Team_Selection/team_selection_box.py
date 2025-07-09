import pygame
from Views_Assets.neon_box import NeonBox
from Team_Selection.team_selection_model import TeamSelectionModel

class TeamSelectionBox:
    def __init__(self, screen, model: TeamSelectionModel):
        self.screen = screen
        self.model = model
        
        self.box = NeonBox(
            self.screen,
            position= (self.model.position.x, self.model.position.y),
            object_size= (840, 650),
            overlay_fill_RGBA=(0,0,0,170)
        )
    def render(self):
        self.box.position = (self.model.position.x, self.model.position.y)
        self.box.render()