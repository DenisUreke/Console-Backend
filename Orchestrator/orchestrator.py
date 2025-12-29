import asyncio
import json
from Enums.state_enum import State
from Enums.music_enum import Music
from Enums.game_enum import Game
from Enums.controller_enum import Controller
from Sound_Manager.sound_manager import SoundManager
from Player_Manager.player_manager import PlayerManager
from Message_Parser.message_parser import MessageParser
from Broadcasting_Manager.broadcasting_manager import BroadcastingManager
from Database_Service.database_service import DatabaseService
from Controller_Functions.Controller_Translator.controller_translator import ControllerTranslator
from Lobby.lobby_controller import LobbyController
from Lobby.lobby_view import LobbyView
from Lobby.lobby_model import LobbyModel
from Team_Selection.team_selection_view import TeamSelectionView
from Team_Selection.team_selection_controller import TeamSelectionController
from Team_Selection.team_selection_model import TeamSelectionModel
import time
from Pause_Overlay.pause_overlay_model import PauseOverlayModel
from Pause_Overlay.pause_overlay_controller import PauseOverlayController
from Pause_Overlay.pause_overlay_view import PauseOverlayView



class Orchestrator:
    def __init__(
        self,
        screen,
        sound_manager: SoundManager, 
        player_manager: PlayerManager, 
        message_parser: MessageParser, 
        broadcasting_manager: BroadcastingManager,
        controller_translator: ControllerTranslator,
        database_service: DatabaseService
        ):
        
        self.screen = screen
        self.websocket_server = None
        self.player_manager = player_manager
        self.message_parser = message_parser
        self.database_service = database_service
        self.selected_game = Game.PONG
        self.sound_manager = sound_manager
        self.broadcasting_manager = broadcasting_manager
        self.controller_translator = controller_translator
        self.current_controller = None
        self.current_view = None
        self.is_paused = False
        self.overlay_controller = None
        self.overlay_view = None
        self.controller_url = "http://192.168.1.213:4200/"  # change port/path as needed
        self.qr_surface = None

        # debounce to avoid rapid toggles if button is spammed
        self._last_pause_toggle_ts = 0.0
        self._pause_toggle_debounce_s = 0.20

        self.message_handlers = {
            "player_join": self.handle_player_join,
            "change_leader": self.change_leader,
            "player_controls": self.handle_player_controls,
        }
        self.state_music_map = {
            State.LOBBY: Music.LOBBY,
            State.PONG: Music.NONE,
            State.TEAM_SELECTION: Music.TEAM_SELECTION,
            # Add future mappings here
        }
        
        # Set controller and view factories for each state
        self.controller_factory_map = {
            State.LOBBY: lambda: LobbyController(
                self.screen,
                self,
                self.sound_manager,
                LobbyModel()
        ),
            State.TEAM_SELECTION: lambda: TeamSelectionController(
                self.screen,
                self,
                self.sound_manager,
                TeamSelectionModel()
        ),
            # Add more states/controllers here
        }

        self.view_factory_map = {
            State.LOBBY: lambda model: LobbyView(
                self.screen,
                model,
                self
        ),
            State.TEAM_SELECTION: lambda model: TeamSelectionView(
                self.screen,
                model,
                self
            )
            # Add more states/views here
        }
        
        self.state = State.LOBBY
        
        self.database_service.initialize_schema()
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        
        print(f"[STATE] Switching controller to: {value}")
        # assigning the correct controller based on State
        controller_factory = self.controller_factory_map.get(value)
        if controller_factory:
            controller = controller_factory()
            if self.current_controller:
                self.current_controller.stop()
            self.current_controller = controller
        print(f"[DEBUG] New controller: {controller}")
            
        # assigning the correct View based on State
        view_factory = self.view_factory_map.get(value)
        if view_factory:
            self.current_view = view_factory(controller.model)
            controller.view = self.current_view
            
        print(f"[STATE] Switching view to: {value}")
        print(f"[DEBUG] Controller's model: {controller.model}")
        print(f"[DEBUG] New view: {self.current_view}")
            
        # change the music according to state
        self.change_music_according_to_state(value)
        
        # broadcast the state to frontend
        if self.websocket_server:
            self.websocket_server.broadcast_state_sync()
        
    def handle_message(self, websocket, message):
        data = json.loads(message)
        message_type = data.get("type")
        payload = data.get("data", {})

        handler = self.message_handlers.get(message_type)

        if handler:
            handler(websocket, payload)
        else:
            print(f"Unknown message type: {message_type}")

    def handle_player_join(self, websocket, payload): ### KLAR
        
        name = payload.get("name")
        self.player_manager.create_and_append_player(name, websocket)
        self.broadcast_player_list()
            
    def change_leader(self, websocket, payload): ########### KLAR
        
        name = payload.get("name")
        self.player_manager.change_leader(name)
        self.broadcast_player_list()

    def handle_player_disconnect(self, websocket): ### KLAR
        
        self.player_manager.update_list_by_websocket_connections(websocket)
        self.player_manager.re_assign_leader()
        self.broadcast_player_list()
        print("Player disconnected and removed")
        
        if len(self.player_manager.players) == 0:
            # pause only if we aren't already paused
            if not self.is_paused:
                self.toggle_pause(paused_by_player_number=None)
        
        # function that handles player input
    def handle_player_controls(self, websocket, payload):
        translated_payload = self.controller_translator.get_extracted_controller_values(
            state=self.state,
            payload=payload
        )

        if not translated_payload:
            return

        # 1) Pause toggle always works
        if translated_payload.get("type") == "pause_toggle":
            self.toggle_pause(translated_payload.get("player_number"))
            return

        # 2) If paused, block base input (only overlay can react)
        if self.is_paused:
            if self.overlay_controller:
                self.overlay_controller.handle_input(translated_payload)
            return

        # 3) Normal behavior
        if self.current_controller:
            self.current_controller.handle_input(translated_payload)
    
    def broadcast_player_list(self): #### Klar
        
        message_json = self.message_parser.get_parsed_player_list(self.player_manager)
        self.broadcasting_manager.broadcast_to_all_connected(self.websocket_server, message_json)
                             
    def set_state(self, state):
            print(f"Changing state to: {state}")
            self.state = state
            
    # ----------------Handle music-------------------------
            
    def change_music_according_to_state(self, state: State):
        music_enum = self.state_music_map.get(state, None)
        
        if music_enum==Music.NONE:
            self.stop_music()
        else:
            self.play_music(music_enum= music_enum)
            
        
    def play_music(self, music_enum, loop=-1):
        self.stop_music()
        self.sound_manager.play_music(music_enum.value, loop)
    
    def stop_music(self):
        self.sound_manager.stop_music()

    # -------------Handle Controller Change-----------------
    
    def set_controller(self, controller_type: Controller, player_number = "all"):
        
        message_json = self.message_parser.get_parsed_change_controller(controller_type, player_number)
        self.broadcasting_manager.broadcast_to_all_connected(self.websocket_server, message_json)
        
    def set_selected_game(self, game: Game):
        self.selected_game = game
        print(f"[DEBUG] Selected game set to: {self.selected_game}")
        
    # -------------Pause Functionality-----------------
    
    def toggle_pause(self, paused_by_player_number=None):
        now = time.monotonic()
        if (now - self._last_pause_toggle_ts) < self._pause_toggle_debounce_s:
            return
        self._last_pause_toggle_ts = now

        # --- Turn ON pause ---
        if not self.is_paused:
            self.is_paused = True

            # Ensure QR is generated once
            if self.qr_surface is None:
                from QR_Code.make_qr_surface import make_qr_surface
                self.qr_surface = make_qr_surface(self.controller_url, size_px=260)

            model = PauseOverlayModel(
                paused_by_player_number=paused_by_player_number,
                url=self.controller_url
            )
            self.overlay_controller = PauseOverlayController(self, model)
            self.overlay_view = PauseOverlayView(self.screen, model, self.qr_surface)
            self.sound_manager.set_music_volume(0.1)  # lower music volume when paused

        # --- Turn OFF pause ---
        else:
            self.is_paused = False
            if self.overlay_controller:
                self.overlay_controller.stop()
            self.overlay_controller = None
            self.overlay_view = None
            self.sound_manager.set_music_volume(1)

        # optional: tell clients pause state changed
        if getattr(self, "websocket_server", None):
            self.websocket_server.broadcast_state_sync()


    
    
                
        
        