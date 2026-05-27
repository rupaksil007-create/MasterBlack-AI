from fastapi import APIRouter
from backend.app.api.v1.endpoints import ws

api_router = APIRouter()

api_router.include_router(ws.router, prefix="/ws", tags=["websockets"])
