import asyncio
import json
from Enums.state_enum import State
from Enums.music_enum import Music
from Enums.controller_enum import ControllerType
from Sound_Manager.sound_manager import SoundManager
from Player_Manager.player_manager import PlayerManager
from Message_Parser.message_parser import MessageParser
from Broadcasting_Manager.broadcasting_manager import BroadcastingManager



class Orchestrator:
    def __init__(self, sound_manager: SoundManager, player_manager: PlayerManager, message_parser: MessageParser, broadcasting_manager: BroadcastingManager):
        self.websocket_server = None
        self.player_manager = player_manager
        self.message_parser = message_parser
        self.selected_game = State.LOBBY
        self.sound_manager = sound_manager
        self.broadcasting_manager = broadcasting_manager
        
        self._state = State.LOBBY

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
        self.state_controller_map = {
            State.LOBBY: ControllerType.STANDARD_CONTROLLER
        }
        
        self.selected_controller = self.state_controller_map.get(self._state, ControllerType.STANDARD_CONTROLLER)
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
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
        
        # function that handles player input
    def handle_player_controls(self, websocket, payload):
        
        self.game_master.handle_player_controls(payload, websocket)
        
    
    def broadcast_player_list(self): #### Klar
        
        message_json = self.message_parser.get_parsed_player_list(self.player_manager)
        self.broadcasting_manager.broadcast_player_list_async(self.websocket_server, message_json)
                             
    def change_state(self, state):
        if self.state == State.LOBBY:
            self.selected_game = state
            self.state = State.TEAM_SELECTION
        else:
            self.state = state
            
    def change_music_according_to_state(self, state: State):
        music_enum = self.state_music_map.get(state, None)
        
        if music_enum==Music.NONE:
            self.stop_music()
        else:
            self.play_music(music_enum= music_enum)
            
        
    def play_music(self, music_enum, loop=-1):
        self.sound_manager.play_music(music_enum.value, loop)
    
    def stop_music(self):
        self.sound_manager.stop_music()
                
        
        