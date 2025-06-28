from Models.player import Player

class PlayerManager:
    def __init__(self):
        self.players: list[Player] = []
        self.next_player_number = 1
        
    def create_and_append_player(self, name, websocket):
        
        is_leader = self.assign_leader()
    
        player = Player(websocket, name, self.next_player_number, is_leader)    
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
        