import pygame
from Enums.game_enum import Game
from Orchestrator.orchestrator import Orchestrator

class GameList:
    def __init__(self, screen, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.screen = screen
        self.games: Game = orchestrator.game_master.lobby_controller.lobby_model.game_list
        self.font = pygame.font.Font(None, 36)
        pygame.font.init()
        
    def update(self):
        pass
    
    def render(self):
        y = 100
        for game in self.games:
            if self.orchestrator.game_master.lobby_controller.lobby_model.current_game_selected == game:
                self.font.set_bold(True)
                color = (255, 255, 255)
            else:
                self.font.set_bold(False)
                color = (0, 255, 255)
            text = self.font.render(game.value, True, color)
            self.screen.blit(text, (990, y))
            y += 40
            