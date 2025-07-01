import pygame
import time
import threading
from main_init import initialize_game

# initializing and delegating from main_init
components = initialize_game()
orchestrator = components["orchestrator"]
server = components["server"]
clock = components["clock"]

# Start the server (it will create its own thread internally)
server.start()
time.sleep(1)
print("WebSocket server should be running on ws://192.168.0.31:8765")


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
        
        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    # Clean shutdown
    server.stop()
    pygame.quit()
    print("Application closed")
