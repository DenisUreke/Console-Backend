import asyncio

class BroadcastingManager():
    def __init__(self):
        pass

    def broadcast_to_all_connected(self, websocket_server, message_json):
        if websocket_server:
            # Create tasks for all clients
            for websocket in websocket_server.clients:
                try:
                    # Use asyncio to send the message
                    asyncio.create_task(websocket.send(message_json))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")