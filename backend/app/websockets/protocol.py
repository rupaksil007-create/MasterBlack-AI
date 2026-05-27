from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

class EventType(str, Enum):
    LOG = "log"
    TERMINAL = "terminal"
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"
    AGENT_THOUGHT = "agent_thought"
    FILE_CHANGE = "file_change"
    ERROR = "error"

class WebSocketMessage(BaseModel):
    type: EventType
    session_id: str
    data: Dict[str, Any]
    timestamp: float = Field(default_factory=lambda: __import__("time").time())

class LogMessage(BaseModel):
    level: str
    message: str

class TerminalMessage(BaseModel):
    content: str

class ToolResultMessage(BaseModel):
    tool_name: str
    result: Any
    success: bool
