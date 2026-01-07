import pygame

class TeamSelectionModel:
    def __init__(self):
        
        '''Game ready values'''
        self.game_ready = False
        
        '''Animation values'''
        self.screen_width = 1280
        self.screen_height = 720
        self.starting_position = pygame.Vector2(self.screen_width//2 -350, self.screen_height//2 -1000)
        self.ending_position = pygame.Vector2(self.screen_width//2 -350, self.screen_height//2-270)
        self.position = self.starting_position.copy()
        self.speed = 10
        self.start_moving = True
        
    def update_ending_position(self):
        self.ending_position = pygame.Vector2(
            self.screen_width // 2 - 350,
            self.screen_height // 2 - 270 * 4
        )
    
    def toggle_game_ready(self, value: bool):
        self.game_ready = value