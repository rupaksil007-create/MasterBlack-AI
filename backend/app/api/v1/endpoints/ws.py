import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.websockets.manager import manager
from backend.app.agents.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    orchestrator = get_orchestrator(session_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                user_input = message.get("text", "")
                
                # Hand off to orchestrator
                if user_input:
                    # We run this as a background task to not block the WS loop
                    import asyncio
                    asyncio.create_task(orchestrator.process_request(user_input))
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from session {session_id}")
            except Exception as e:
                logger.error(f"Error processing WS message: {e}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        logger.info(f"Session {session_id} disconnected")
