from Enums.game_enum import Game
import pygame

class LobbyModel:
    def __init__(self):
        self.game_list: Game = Game
        self.current_game_selected = Game.PONG
        
        # middle-screen data
        self.starting_pos = pygame.Vector2(400, -800)
        self.end_pos = pygame.Vector2(400, 50)
        self.position = self.starting_pos.copy()
        self.ms_speed = 10
        self.ms_start_moving = True
        
        

        