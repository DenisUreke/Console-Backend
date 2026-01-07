import pygame
from Interfaces.view_interface import ViewInterface
from Lobby.lobby_player_list import PlayerList
from Lobby.lobby_game_list import GameList
from Lobby.lobby_middle_box import MiddleBox
from Views_Assets.neon_box import NeonBox
from Enums.image_path_enum import ImagePath
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class LobbyView(ViewInterface):
    def __init__(self, screen, model, orchestrator: 'Orchestrator'):
        self.screen = screen
        self.model = model
        self.orchestrator = orchestrator
        self.show_game_settings_box = True
        
        self.player_box = NeonBox(screen, overlay_fill_RGBA=(0,0,0,170), position=(56, 90))
        self.game_box = NeonBox(screen, overlay_fill_RGBA=(0,0,0,170), position=(921, 90))
        
        self.player_list = PlayerList(screen, orchestrator)
        self.game_settings_box = MiddleBox(screen, model)
        self.game_list = GameList(screen, model)
        
        # Load background image
        image_path = ImagePath.get_image_path(self.orchestrator.state)
        original_bg = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(original_bg, self.screen.get_size())
    
    def update(self, dt_ms: int):
        pass
        
    def render(self):
        
        # First draw background idiot
        self.screen.blit(self.background, (0, 0))
        
        # self.screen.fill((0, 0, 0))

        self.player_box.render()
        self.player_list.render()
        self.game_box.render()
        self.game_list.render()
        
        if self.show_game_settings_box:
            self.game_settings_box.render()