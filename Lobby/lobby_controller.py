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
        event_type = event.get("type")
        
        match event_type:
            case "joystick_move":
                translated_direction = event.get("translated_direction")
                direction = event.get("direction")
                distance = event.get("distance")
                player_number = event.get("player_number")
                self.handle_joystick_move(translated_direction, direction, distance, player_number)
                
            case "joystick_release":
                released = event.get("released")
                player_number = event.get("player_number")
                self.handle_joystick_release(released, player_number)
                              
            case "button_press":
                button = event.get("button")
                player_number = event.get("player_number")
                self.handle_button_click(button, player_number)
                
            case _:
                print(f"Unknown event type: {event_type}")

    def update(self):
        
        if self.model.ms_start_moving:
            direction = self.model.end_pos - self.model.position
            if direction.length() < self.model.ms_speed:
                self.model.position = self.model.end_pos
                self.moving = False
            else:
                self.model.position += direction.normalize() * self.model.ms_speed
    
    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
    
    def update_game(self, index):
        game_list = list(Game)
        if 0 <= index < len(game_list):
            self.model.current_game_selected = game_list[index]
        
    def change_selected_game(self, current: Game):
        self.model.current_game_selected = current
    
    def handle_joystick_move(self, translated_directon, direction, distance, player_number):
        if direction == "up" and distance > 50 or direction == "down" and distance > 50:
            self.model.current_selected_game(direction)
    
    def handle_joystick_release(self, release, player_number):
        pass
    
    def handle_button_click(self, button, player_number):
        pass
    
        