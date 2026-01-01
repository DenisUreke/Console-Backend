from Models.player import Player
from Enums.colors_enum import COLOR_LIST
import secrets

class PlayerManager:
    def __init__(self):
        self.players: list[Player] = []
        self.next_player_number = 1
        
    def handle_player_join(self, name, websocket, session_token):
        if session_token:
            player = self.get_player_by_session_token(session_token)
            if player:
                player.name = name
                player.websocket = websocket
                player.connected = True
                print(f"[SESSION]Player re-joined: {player.name} as Player {player.player_number} and token {session_token}")
                return
        else:
            self.create_and_append_player(name, websocket)
        
    def create_and_append_player(self, name, websocket):
        
        is_leader = self.assign_leader()
        color_theme = self.get_color_theme()
        session_token = self.get_session_token()
        print(f"[SESSION]Generated session token for {name}: {session_token}")
        
        player = Player(websocket=websocket, 
                        name=name, 
                        player_number=self.next_player_number, 
                        is_in_game=False, 
                        is_leader=is_leader, 
                        color_theme=color_theme,
                        session_token = session_token,
                        connected = True
                        )    
        
        self.players.append(player)
        self.next_player_number += 1
        
        leader_text = " (LEADER)" if is_leader else ""
        print(f"[SESSION]Player joined: {name} as Player {player.player_number}{leader_text}")
        
    def assign_leader(self):
        return len(self.players) == 0
    
    def get_player(self, name):
        return next((p for p in self.players if p.name == name), None)
    
    def change_leader(self, name):
        player = self.get_player(name)
        
        if player:
            for p in self.players:
                p.is_leader = False
            player.is_leader = True
        print(f"Leader changed to: {name}")
        
    def re_assign_leader(self):
        if len(self.players) > 0 and not any(player.is_leader for player in self.players):
            for player in self.players:
                if player.is_leader == False and player.connected:
                    player.is_leader = True
                    return
            
    def update_list_by_websocket_connections(self, websocket):
        
        for p in self.players:
            if p.websocket == websocket:
                p.connected = False
                if p.is_leader:
                    p.is_leader = False
        
        
    def is_leader(self, player_number):
        player = next((p for p in self.players if p.player_number == player_number), None)
        return player.is_leader if player else False
    
    def evaluate_teamselection_position(self, position: int, direction: str) -> int:
        delta = {
            "left": -1,
            "right": 1
        }.get(direction, 0)
        new_value = position + delta
        new_value = max(0, min(2, new_value))
        return new_value
    
    def set_team_selection_position(self, player_number: int, direction: str):
        player = next((p for p in self.players if p.player_number == player_number), None)
        if player:
            position = self.evaluate_teamselection_position(player.team_selection_position, direction)
            player.team_selection_position = position
            #print(f"Player {player.name} team selection position set to {position}")
    
    def get_color_theme(self ) -> str:
        idx = len(self.players) % len(COLOR_LIST)
        return COLOR_LIST[idx].value
    
    def get_session_token(self)-> str:
        return secrets.token_hex(16)
    
    def get_player_by_session_token(self, session_token: str) -> Player | None:
        return next((p for p in self.players if p.session_token == session_token), None)        
        
 