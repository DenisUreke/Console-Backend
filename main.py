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

        # -------------------- UPDATE --------------------
        if orchestrator.is_paused:
            # Freeze EVERYTHING except the pause overlay itself
            if orchestrator.pause_overlay_controller:
                orchestrator.pause_overlay_controller.update(dt_ms)  # optional if you have it
            if orchestrator.pause_overlay_view:
                orchestrator.pause_overlay_view.update(dt_ms)        # optional if your views use update
        else:
            # Base game updates
            if orchestrator.current_controller:
                orchestrator.current_controller.update()  # later you can pass dt_ms

            # Game overlay updates (dice/question/etc.) while NOT paused
            if orchestrator.overlay_controller:
                orchestrator.overlay_controller.update(dt_ms)   # or update()

            # Views update (animations/camera easing live here if you want)
            if orchestrator.current_view:
                orchestrator.current_view.update(dt_ms)

            if orchestrator.overlay_view:
                orchestrator.overlay_view.update(dt_ms)

        # -------------------- RENDER --------------------
        if orchestrator.current_view:
            orchestrator.current_view.render()

        if orchestrator.overlay_view:
            orchestrator.overlay_view.render()

        if orchestrator.is_paused and orchestrator.pause_overlay_view:
            orchestrator.pause_overlay_view.render()

        # -------------------- PRESENT --------------------
        scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()


except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    server.stop()
    pygame.quit()
    print("Application closed")
