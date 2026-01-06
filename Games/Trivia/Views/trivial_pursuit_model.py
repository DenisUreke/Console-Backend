import pygame
from Games.Trivia.Models.trivia_game_models import RingTile
from Games.Trivia.Models.tpp_player_model import TPPlayer, TPPlayerToken
from Games.Trivia.Models.trivia_send_to_front_end import PossibleMove, PossibleMovesData
from Games.Trivia.Enums_Trivia.trivia_camera_mode_enum import TriviaCameraModeEnum
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
from Games.Trivia.Helpers.build_ring_tiles import build_ring_tiles
from Games.Trivia.Enums_Trivia.trivia_tile_type import StartingLocations, TileType
from Games.Trivia.Enums_Trivia.trivia_categories_enum import TPWedgeCategory, WEDGE_TO_API, COLOR_TO_WEDGE_CATEGORY, API_TO_WEDGE, WEDGE_CATEGORY_TO_COLOR, WedgeColor
from typing import List, Optional
from enum import Enum

class DiceOverlayPhase(Enum):
    PROMPT = "prompt"   # show "Press X to roll"
    ROLLING = "rolling" # play animation
    RESULT = "result"   # show final face, wait for confirmation


class TriviaPursuitModel:
    def __init__(self):
        self.ring_tiles: List[RingTile] = build_ring_tiles()
        self.players: List[TPPlayer] = []
        self.current_player_turn: int | None = None
        self.phase = TPPhase.AWAIT_ROLL # <-- current game phase
        self.current_tile = None
        
        ##### Camera values ######
        
        # Current camera positions
        self.camera_x = 0
        self.camera_y = 0
        # Where we want the camera to go
        self.camera_target_x = 0
        self.camera_target_y = 0
        # (FOLLOW vs TRANSITION)
        self.camera_mode = TriviaCameraModeEnum.FOLLOW
        # Speed of camera movement
        self.camera_speed_px_per_sec = 900
        
        # World and viewport sizes
        self.world_width = 1920
        self.world_height = 1915
        self.viewport_width = 960
        self.viewport_height = 640
        
        # Dice assets
        self.dice_phase = DiceOverlayPhase.PROMPT
        self.dice_value: int | None = None
        
        # Movement assets
        self.display_possible_moves: bool = False
        self.possible_move_indices: List[int] = []

        
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
        
            
    def get_current_player(self) -> TPPlayer | None:
        # return player depending on player number
        if self.current_player_turn is None:
            return None
        return next((p for p in self.players if p.player_number == self.current_player_turn), None)
    
    def set_starting_player(self):
        if self.players:
            self.current_player_turn = self.players[0].player_number

    def set_next_player_turn(self):
        if not self.players or self.current_player_turn is None:
            return

        current_index = next((i for i, p in enumerate(self.players)
                            if p.player_number == self.current_player_turn), None)
        if current_index is None:
            return

        next_index = (current_index + 1) % len(self.players)
        next_player = self.players[next_index]

        # 1) switch active player
        self.current_player_turn = next_player.player_number

        # 2) switch camera mode to transition
        self.camera_mode = TriviaCameraModeEnum.TRANSITION

        # 3) compute centered camera target for that player (Step B math)
        half_w = self.viewport_width / 2
        half_h = self.viewport_height / 2
        max_x = self.world_width - self.viewport_width
        max_y = self.world_height - self.viewport_height

        tx = next_player.player_token.x - half_w
        ty = next_player.player_token.y - half_h

        # clamp (reuse your clamp helper if it's in the model; otherwise do it inline)
        self.camera_target_x = max(0, min(tx, max_x))
        self.camera_target_y = max(0, min(ty, max_y))
        
    def set_new_player_location_(self):
        pass
    
    def get_possible_moves(self, dice_value: int) -> List[int]:
        possible_indices = []
        current_player = self.get_current_player()
        if not current_player:
            return possible_indices
        
        start_index = current_player.ring_index
        ring_size = len(self.ring_tiles)
        
        # Clockwise
        cw_index = (start_index + dice_value) % ring_size
        possible_indices.append(cw_index)
        
        # Counter-Clockwise
        ccw_index = (start_index - dice_value + ring_size) % ring_size # + ring to ensure we dont get a negative value, you idiot (talking to myself =))
        if ccw_index != cw_index:
            possible_indices.append(ccw_index)
        
        return possible_indices
    
    def build_possible_moves_data(self, dice_value: int, possible_indices: list[int]) -> PossibleMovesData:
        moves: list[PossibleMove] = []

        for idx in possible_indices:
            tile = self.ring_tiles[idx]

            moves.append(PossibleMove(
                index=idx,
                tile_type=tile.tile_type.name,
                category=(tile.category.name if tile.category else None)
            ))

        return PossibleMovesData(dice_value=dice_value, moves=moves)


    


    


            
            
    
    
