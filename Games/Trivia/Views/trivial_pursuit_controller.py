from unittest import case
from Games.Trivia.Views.trivial_pursuit_model import TriviaPursuitModel
from Games.Trivia.Models.trivia_game_models import RingTile
from Interfaces.controller_interface import ControllerInterface
from Enums.overlay_enum import OverlayState
from Enums.controller_enum import Controller
from Games.Trivia.Enums_Trivia.trivia_camera_mode_enum import TriviaCameraModeEnum
from Games.Trivia.Views.trivial_pursuit_model import DiceOverlayPhase
from Games.Trivia.Enums_Trivia.trivia_state_enum import TPPhase
from Enums.state_enum import State
from Games.Trivia.Enums_Trivia.trivia_tile_type import TileType
from Api_Handler.api_caller import ApiCaller
from Games.Trivia.Gateway.trivia_gateway import TriviaGateway, TriviaGatewayError
from Games.Trivia.Models.trivia_models import TriviaRequest, TriviaDifficulty, TriviaCategory
from Games.Trivia.Enums_Trivia.trivia_categories_enum import TP_TO_TRIVIA_CATEGORY, TPWedgeCategory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Orchestrator.orchestrator import Orchestrator

class TrivialPursuitController(ControllerInterface):
    def __init__(self, screen, orchestrator: 'Orchestrator', sound_manager, model: TriviaPursuitModel):
        self.screen = screen
        self.orchestrator = orchestrator
        self.sound_manager = sound_manager
        self.model = model
        
        # Api handling setup 
        api = ApiCaller(base_url="https://the-trivia-api.com", timeout_seconds=6.0)
        self.trivia_gateway = TriviaGateway(api)
        
    def start(self):
        '''Initialize game state, variables, assets'''
        for player in self.orchestrator.player_manager.players:
            if player.connected and player.is_in_game:
                self.model.add_player_to_game(
                    player_name=player.name, 
                    player_number=player.player_number, 
                    color=player.color_theme, 
                    websocket_id=player.websocket
                    )
                
        self.model.set_starting_positions()
        self.model.set_starting_player()
        self.orchestrator.set_controller(Controller.TRIVIA)
        self.orchestrator.overlay_state = OverlayState.NONE

    def stop(self):
        '''Clean up resources, stop threads/timers'''
        pass

    def handle_input(self, event):
        '''Handle input from user'''
        event_type = event.get("type")
        player_number = event.get("player_number")
            
        match event_type: 
            case "button_press":
                button = event.get("button")
                player_number = event.get("player_number")
                self.handle_button_click(button, player_number)
                
            case "keypad_move":
                direction = event.get("direction")
                player_number = event.get("player_number")
                self.handle_keypad_move(direction, player_number)
                    
            case _:
                print(f"Unknown event type: {event_type}")

    def update(self):
        '''Update game logic (movement, collisions, scores)'''
        pass

    def handle_fx(self, event_name: str):
        '''Play sounds associtiated with game events'''
        pass
    
    def handle_button_click(self, button, player_number):
        
        match self.orchestrator.state:
            
          case State.TRIVIA_LOBBY:
            self.start()
            self.orchestrator.state = State.TRIVIA
            return
            
          case State.TRIVIA:
            match self.model.phase:
                case TPPhase.AWAIT_ROLL:
                    if button == 'X':
                        self.orchestrator.set_overlay_state(OverlayState.TRIVIA_DICE_ROLL)
                        return
                case TPPhase.CHOOSE_MOVE:
                    self.move_player_token(button, player_number)
                    self.handle_new_tile_location_action(button, player_number)
                    return

    def handle_keypad_move(self, direction, player_number):
        pass
    
    def get_ring_tile_at_index(self, index: int) -> RingTile | None:
        if index < 0 or index >= len(self.model.ring_tiles):
            return None
        return self.model.ring_tiles[index]
    
    def move_player_token(self, button, player_number):
        button_value = int(button)
        self.update_token_location(player_number, button_value)
        self.model.phase = TPPhase.MOVING
        self.model.set_camera_mode(TriviaCameraModeEnum.FOLLOW)
        
    def update_token_location(self, player_number: int, tile_index: int):
        player = next((p for p in self.model.players if p.player_number == player_number), None)
        if player is None:
            return
        chosen_tile:RingTile = self.get_ring_tile_at_index(tile_index)
        player.player_token.target_x = chosen_tile.x
        player.player_token.target_y = chosen_tile.y
    
    def handle_new_tile_location_action(self, button, player_number):
        button_value = int(button)
        chosen_tile:RingTile = self.get_ring_tile_at_index(button_value)
        
        match chosen_tile.tile_type:
            case TileType.NORMAL | TileType.WEDGE:
                self.handle_guestion_sending(chosen_tile)
            case TileType.ROLL_AGAIN:
                self.set_roll_phase()            
            
    def set_roll_phase(self):
        self.model.phase = TPPhase.AWAIT_ROLL
        self.model.set_camera_mode(TriviaCameraModeEnum.TRANSITION)
        self.orchestrator.set_overlay_state(OverlayState.TRIVIA_DICE_ROLL)
        
    def tile_to_trivia_request(self, chosen_tile: RingTile) -> TriviaRequest:
        raw = getattr(chosen_tile, "category", None)  # TPWedgeCategory or TriviaCategory or None

        if raw is None:
            category = TriviaCategory.general_knowledge
        elif isinstance(raw, TriviaCategory):
            category = raw
        else:
            category = TP_TO_TRIVIA_CATEGORY.get(raw, TriviaCategory.general_knowledge)

        return TriviaRequest(
            limit=1,
            categories=[category],
            region="SE",
            tags=[],
    )
        
    def handle_guestion_sending(self, chosen_tile: RingTile):
        try:
            req = self.tile_to_trivia_request(chosen_tile)
            questions = self.trivia_gateway.get_questions(req)

            if not questions:
                # handle no questions returned--- later =)
                print("No question returned.")
                return

            print(f"Question fetched: {questions[0].question} Answers: {questions[0].answers}, Correct: {questions[0].correct_index}")
            
            # set question values in model
            self.model.set_question_values(questions[0])
            self.model.phase = TPPhase.QUESTION
            self.orchestrator.set_overlay_state(OverlayState.TRIVIA_QUESTION)
            

        except TriviaGatewayError as e:
            print(f"Trivia API failed: {e}")

    
    def handle_question_answered(self):
        pass
        
        