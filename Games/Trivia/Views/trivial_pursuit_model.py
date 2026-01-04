import pygame
from Games.Trivia.Models.trivia_game_models import RingTile
from Games.Trivia.Models.tpp_player_model import TPPlayer, TPPlayerToken
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
from Games.Trivia.Helpers.build_ring_tiles import build_ring_tiles
from Games.Trivia.Enums_Trivia.trivia_tile_type import StartingLocations, TileType
from Games.Trivia.Enums_Trivia.trivia_categories_enum import TPWedgeCategory, WEDGE_TO_API, COLOR_TO_WEDGE_CATEGORY, API_TO_WEDGE, WEDGE_CATEGORY_TO_COLOR, WedgeColor
from typing import List, Optional


class TriviaPursuitModel:
    def __init__(self):
        self.ring_tiles: List[RingTile] = build_ring_tiles()
        self.players: List[TPPlayer] = []
        self.current_player = None
        self.phase = TPPhase.LOBBY
        self.current_tile = None
        
        self.dice_value: int = 1
        
    def add_player_to_game(self, player_number: int, player_name: str, color: str, websocket_id: str):
        new_player = TPPlayer(
            player_number=player_number,
            name=player_name,
            color_theme=color,
            websocket_id=websocket_id
        )
        self.players.append(new_player)
    
    def set_starting_positions(self):    
        for index, player in enumerate(self.players):
            location_idx = list(StartingLocations)[index % len(StartingLocations)].value
            player.player_token.x = self.ring_tiles[location_idx].x
            player.player_token.y = self.ring_tiles[location_idx].y
            player.player_token.target_x = self.ring_tiles[location_idx].x
            player.player_token.target_y = self.ring_tiles[location_idx].y
            player.ring_index = location_idx
            
            
    
    
