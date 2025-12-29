import asyncio
import websockets
import json
import logging
import threading
from Orchestrator.orchestrator import Orchestrator
from Enums.state_enum import State

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketServer:
    def __init__(self, orchestrator, host="192.168.1.213", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.orchestrator = orchestrator
        self.server = None
        self.loop = None

    async def handler(self, websocket, path=None):
        logger.info(f"New client connected from {websocket.remote_address}")
        self.clients.add(websocket)

        try:
            # Send current state on connect
            await self.send_state(websocket)

            # Process incoming messages from the client
            async for message in websocket:
                logger.info(f"[WebSocket] Received message: {message}")
                await self.process_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected normally")
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"WebSocket error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in handler: {e}")
        finally:
            # Clean up client on disconnect
            if websocket in self.clients:
                self.clients.remove(websocket)
            self.orchestrator.handle_player_disconnect(websocket)
            logger.info("Client cleanup completed")

    async def process_message(self, websocket, message):
        logger.info(f"[WebSocket] Processing message: {message}")
        try:
            # Parse JSON if message is a string
            if isinstance(message, str):
                parsed_message = json.loads(message)
            else:
                parsed_message = message
                
            # Process the message with orchestrator
            self.orchestrator.handle_message(websocket, parsed_message)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {e}")
            await self.send_error(websocket, "Invalid JSON format")
        except Exception as e:
            logger.error(f"Error processing message EEEEEE: {e}")
            await self.send_error(websocket, "Error processing message")

    async def send_state(self, websocket):
        try:
            state_message = {
                "type": "state_change",
                "data": {"state": self.orchestrator.state.value}
            }
            await websocket.send(json.dumps(state_message))
            logger.info(f"Sent state to client: {state_message}")
        except Exception as e:
            logger.error(f"Error sending state: {e}")

    async def send_error(self, websocket, error_message):
        try:
            error_response = {
                "type": "error",
                "data": {"message": error_message}
            }
            await websocket.send(json.dumps(error_response))
        except Exception as e:
            logger.error(f"Error sending error message: {e}")

    async def broadcast_state(self):
        if not self.clients:
            logger.info("No clients to broadcast to")
            return
            
        message = {
            "type": "state_change",
            "data": {"state": self.orchestrator.state.value}
        }
        message_json = json.dumps(message)
        
        # Create a list of tasks for broadcasting
        tasks = []
        disconnected_clients = set()
        
        for client in self.clients.copy():
            try:
                tasks.append(client.send(message_json))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error preparing broadcast for client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected_clients
        
        # Execute all send operations
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
                logger.info(f"Broadcasted state to {len(tasks)} clients")
            except Exception as e:
                logger.error(f"Error during broadcast: {e}")

    def broadcast_state_sync(self):
        """Thread-safe method to broadcast state from main thread"""
        if self.loop and not self.loop.is_closed():
            asyncio.run_coroutine_threadsafe(self.broadcast_state(), self.loop)

    async def _run_server(self):
        try:
            # Updated handler function for newer websockets library
            async def connection_handler(websocket):
                await self.handler(websocket, "/")  # Use default path
            
            self.server = await websockets.serve(
                connection_handler, 
                self.host, 
                self.port,
                ping_interval=20,
                ping_timeout=10,
                close_timeout=10
            )
            logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
            
            # Keep the server running
            await self.server.wait_closed()
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise

    def start(self):
        """Start the WebSocket server in a separate thread"""
        def run_server():
            # Create a new event loop for this thread
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            try:
                logger.info(f"Starting WebSocket server on ws://{self.host}:{self.port}")
                self.loop.run_until_complete(self._run_server())
            except Exception as e:
                logger.error(f"Server error: {e}")
            finally:
                logger.info("WebSocket server stopped")

        # Start server in a separate thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        logger.info("WebSocket server thread started")

    def stop(self):
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

