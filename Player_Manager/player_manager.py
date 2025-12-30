from Models.player import Player
from Enums.colors_enum import COLOR_LIST

class PlayerManager:
    def __init__(self):
        self.players: list[Player] = []
        self.next_player_number = 1
        
    def create_and_append_player(self, name, websocket):
        
        is_leader = self.assign_leader()
        color_theme = self.get_color_theme()
        
        player = Player(websocket=websocket, 
                        name=name, 
                        player_number=self.next_player_number, 
                        is_in_game=False, 
                        is_leader=is_leader, 
                        color_theme=color_theme)    
        
        self.players.append(player)
        self.next_player_number += 1
        
        leader_text = " (LEADER)" if is_leader else ""
        print(f"Player joined: {name} as Player {player.player_number}{leader_text}")
        
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
            self.players[0].is_leader = True
            
    def update_list_by_websocket_connections(self, websocket):
        new_list = []
        
        for p in self.players:
            if p.websocket != websocket:
                new_list.append(p)
        
        self.players = new_list
        
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
        
 