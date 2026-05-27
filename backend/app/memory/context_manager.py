from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class Message(BaseModel):
    role: str # user, assistant, system, tool
    content: str
    name: Optional[str] = None # For tool results
    timestamp: float = Field(default_factory=time.time)

class ConversationContext:
    def __init__(self, session_id: str, max_history: int = 20):
        self.session_id = session_id
        self.max_history = max_history
        self.messages: List[Message] = []

    def add_message(self, role: str, content: str, name: Optional[str] = None):
        self.messages.append(Message(role=role, content=content, name=name))
        # Sliding window
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        return [
            {"role": m.role, "content": m.content}
            for m in self.messages
        ]

    def clear(self):
        self.messages = []

# Global store for conversation contexts
_contexts: Dict[str, ConversationContext] = {}

def get_context(session_id: str) -> ConversationContext:
    if session_id not in _contexts:
        _contexts[session_id] = ConversationContext(session_id)
    return _contexts[session_id]
