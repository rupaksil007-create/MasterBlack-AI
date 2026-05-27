import json
import logging
from typing import Dict, List, Any
from fastapi import WebSocket
from backend.app.websockets.protocol import WebSocketMessage

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # session_id -> list of active websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
        logger.info(f"Client connected to session {session_id}. Total connections: {len(self.active_connections[session_id])}")

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        logger.info(f"Client disconnected from session {session_id}")

    async def send_message(self, message: WebSocketMessage):
        session_id = message.session_id
        if session_id in self.active_connections:
            dead_connections = []
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message.model_dump())
                except Exception as e:
                    logger.error(f"Error sending message to session {session_id}: {e}")
                    dead_connections.append(connection)
            
            # Clean up dead connections
            for dead in dead_connections:
                self.active_connections[session_id].remove(dead)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast_to_session(self, session_id: str, message_data: Dict[str, Any]):
        """Broadcasts a raw message to all clients in a session."""
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message_data)
                except Exception:
                    pass

manager = ConnectionManager()
