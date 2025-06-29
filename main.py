import threading
import pygame
import time
from lobby.lobby import Lobby
from team_selection.team_selection_view import TeamSelection
from games.pong.pong_view import Pong
from enums.state_enum import State
from main_init import initialize_game

# initializing from main_init
components = initialize_game()
orchestrator = components["orchestrator"]
server = components["server"]

# Start the server (it will create its own thread internally)
server.start()
time.sleep(1)
print("WebSocket server should be running on ws://192.168.0.31:8765")

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Lobby")
clock = pygame.time.Clock()
pygame.font.init()

# init the different views
lobby = Lobby(screen, orchestrator)
team_selection = TeamSelection(screen, orchestrator)
pong = Pong(screen, orchestrator)

running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if orchestrator.current_controller:
            orchestrator.current_controller.update()

        if orchestrator.current_view:
            orchestrator.current_view.render()

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Clean shutdown
    server.stop()
    pygame.quit()
    print("Application closed")
