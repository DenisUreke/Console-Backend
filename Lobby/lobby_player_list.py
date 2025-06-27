import pygame

class PlayerList:
    def __init__(self, screen, orchestrator):
        self.screen = screen
        self.orchestrator = orchestrator
        self.font = pygame.font.Font(None, 36)

    def render(self):
        y = 100
        for player in self.orchestrator.players:
            # Create the player text
            text = self.font.render(f"{player.name}", True, (0, 255, 255))
            
            # Check if player is leader and add crown
            if player.is_leader:
                crown_text = self.font.render("[L]", True, (255, 215, 0))
                self.screen.blit(crown_text, (70, y))
            
            self.screen.blit(text, (110, y))
            y += 40