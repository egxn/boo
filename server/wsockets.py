from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[(str, WebSocket)] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append((client_id, websocket))

    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove((client_id, websocket))

    async def send_text_update(self, client_id: str, message: str, message_type: str):
        for (client, websocket) in self.active_connections:
            if str(client) == str(client_id):
                await websocket.send_text(message_type + " ::: " + message)
