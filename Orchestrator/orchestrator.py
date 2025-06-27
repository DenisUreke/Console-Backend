import asyncio
import json
from Models.player import Player
from Enums.state_enum import State
from game_master.game_master import GameMaster

class Orchestrator:
    def __init__(self, game_master: GameMaster):
        self.websocket_server = None
        self.players: Player = []
        self.next_player_number = 1
        self.game_master = game_master
        self.selected_game = State.LOBBY
        
        self._state = State.LOBBY

        self.message_handlers = {
            "player_join": self.handle_player_join,
            "change_leader": self.change_leader,
            "player_controls": self.handle_player_controls,
        }
        
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

    def handle_player_join(self, websocket, payload):
        name = payload.get("name")
    
        is_leader = self.assign_leader()
    
        player = Player(websocket, name, self.next_player_number, is_leader)    
        self.players.append(player)
        self.next_player_number += 1
    
        self.broadcast_player_list()
    
        leader_text = " (LEADER)" if is_leader else ""
        print(f"Player joined: {name} as Player {player.player_number}{leader_text}")

    def assign_leader(self):
        return len(self.players) == 0
    
    def re_assign_leader(self):
        if len(self.players) > 0 and not any(player.is_leader for player in self.players):
            self.players[0].is_leader = True
            
    def change_leader(self, websocket, payload):
        name = payload.get("name")
        player = next((p for p in self.players if p.name == name), None)
        if player:
            for p in self.players:
                p.is_leader = False
            player.is_leader = True
            self.broadcast_player_list()
            print(f"Leader changed to: {name}")

    def handle_player_disconnect(self, websocket):
        new_list = []
        
        for p in self.players:
            if p.websocket != websocket:
                new_list.append(p)
        
        self.players = new_list
        self.re_assign_leader()
        self.broadcast_player_list()
        print("Player disconnected and removed")
        
        # function that handles player input
    def handle_player_controls(self, websocket, payload):
        
        self.game_master.handle_player_controls(payload, websocket)
        
    
    def broadcast_player_list(self):
        player_list = []
        for player in self.players:
            player_list.append({
                "name": player.name,
                "player_number": player.player_number,
                "is_leader": player.is_leader,
                "player_score": player.player_score,
                "player_lives": player.player_lives
            })
        message = {
            "type": "player_list_update",
            "data": {
                "players": player_list,
                "player_count": len(self.players)
            }
        }
        # Convert to JSON
        message_json = json.dumps(message)
        
        if self.websocket_server:
        # Create tasks for all clients
            for websocket in self.websocket_server.clients:
                try:
                    # Use asyncio to send the message
                    asyncio.create_task(websocket.send(message_json))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    
    def broadcast_message_from_game_master(self, payload):
        if self.websocket_server:
            
            for websocket in self.websocket_server.clients:
                try:
                    asyncio.create_task(websocket.send(payload))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                             
    def change_state(self, state):
        if self.state == State.LOBBY:
            self.selected_game = state
            self.state = State.TEAM_SELECTION
        else:
            self.state = state
                
        
        