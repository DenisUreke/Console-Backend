import pygame
import time
import threading
from main_init import initialize_game

components = initialize_game()
screen = components["screen"]
game_surface = components["game_surface"]
clock = components["clock"]
orchestrator = components["orchestrator"]
server = components["server"]

# Start the server
server.start()
time.sleep(1)
print("WebSocket server should be running...")

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

        # scale
        scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    server.stop()
    pygame.quit()
    print("Application closed")
