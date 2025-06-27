import pygame
from Enums.game_enum import Game
from Lobby.lobby_model import LobbyModel
from Interfaces.controller_interface import ControllerInterface

class LobbyController(ControllerInterface):
    def __init__(self, screen, orchestrator, sound_manager, model: LobbyModel):
        self.screen = screen
        self.orchestrator = orchestrator
        self.sound_manager = sound_manager
        self.model = model
        
    def start(self):
        '''Initialize game state, variables, assets'''
        pass

    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass

    def handle_input(self, event):
        '''Handle input from user'''
        pass

    def update(self):
        '''Update game logic (movement, collisions, scores)'''
        pass
    
    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
    
    def update_game(self, index):
        game_list = list(Game)
        if 0 <= index < len(game_list):
            self.model.current_game_selected = game_list[index]
        
    def change_selected_game(self, current: Game):
        self.model.current_game_selected = current