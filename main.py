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
        
        dt_ms = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Freeze base updates while paused
        if not orchestrator.is_paused and orchestrator.current_controller:
            orchestrator.current_controller.update()

        # Always render base view
        if orchestrator.current_view:
            orchestrator.current_view.update(dt_ms)
            orchestrator.current_view.render()

        # Render overlay on top (still on game_surface)
        if orchestrator.is_paused and orchestrator.overlay_view:
            orchestrator.overlay_view.render()

        # scale
        scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    server.stop()
    pygame.quit()
    print("Application closed")
