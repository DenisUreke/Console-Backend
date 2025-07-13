from Enums.game_enum import Game
import pygame

class LobbyModel:
    def __init__(self):
        self.game_list = list(Game)
        self.current_game_selected = Game.PONG
        
        # Game list value
        self.index = 0
        
        # middle-screen data
        #self.starting_pos = pygame.Vector2(400, -800)
        #self.end_pos = pygame.Vector2(400, 50)
        self.starting_pos = pygame.Vector2(330, -800)
        self.end_pos = pygame.Vector2(310, 40)
        self.position = self.starting_pos.copy()
        self.ms_speed = 10
        self.ms_start_moving = True
        
    def reset_middle_box(self):
        self.ms_start_moving = False
        self.position = self.starting_pos
        self.ms_start_moving = True
    
    def current_selected_game(self, direction):
        
        if direction == "up":
            self.index -= 1
        if direction == "down":
            self.index += 1
        
        self.index %= len(self.game_list)
        self.current_game_selected = self.game_list[self.index]
            
        
         
        

        