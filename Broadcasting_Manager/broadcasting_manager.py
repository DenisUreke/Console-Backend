import asyncio

class BroadcastingManager():
    def __init__(self):
        pass

    def broadcast_to_all_connected(self, websocket_server, message_json):
        if websocket_server:
            # Create tasks for all clients
            for websocket in websocket_server.clients:
                try:
                    # print(f"Broadcasted player list {message_json}")
                    # Use asyncio to send the message
                    asyncio.create_task(websocket.send(message_json))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    
    def broadcast_to_specific_client(self, websocket, message_json):
        if websocket:
            try:
                print(f"Broadcasted to specific client: {message_json}")
                # Use asyncio to send the message
                asyncio.create_task(websocket.send(message_json))
            except Exception as e:
                print(f"Error broadcasting to specific client: {e}")
                
    def broadcast_to_specific_clients(self, websocket_server, target_websockets, message_json):
        if websocket_server:
            for websocket in target_websockets:
                try:
                    # print(f"Broadcasted to specific client: {message_json}")
                    # Use asyncio to send the message
                    asyncio.create_task(websocket.send(message_json))
                except Exception as e:
                    print(f"Error broadcasting to specific client: {e}")
    