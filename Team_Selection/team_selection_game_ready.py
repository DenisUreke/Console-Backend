import pygame
import math
from Team_Selection.team_selection_model import TeamSelectionModel

class TeamSelectionGameReadyView:
    def __init__(self, screen: pygame.Surface, model: TeamSelectionModel):
        self.screen = screen
        self.model  = model

        # message
        self.message = "Game Ready!"

        # pulsation settings
        self.min_size = 36          
        self.max_size = 56            
        self.freq     = 1.0             
    def render(self):
        
        # compute current font size via a sine wave
        t = pygame.time.get_ticks() / 1000.0 
        # the sine wave oscillates between 0 and 1
        ratio = (math.sin(2 * math.pi * self.freq * t) + 1) / 2 
        # scale the font size between min and max
        size  = int(self.min_size + ratio * (self.max_size - self.min_size))
 
        font = pygame.font.Font(None, size)
        text = font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect()

        x, y = self.model.position.x, self.model.position.y
        text_rect.centerx = x + 350
        text_rect.top     = y + 30

        self.screen.blit(text, text_rect)