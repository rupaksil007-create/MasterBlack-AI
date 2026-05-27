import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
import google.generativeai as genai
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Any:
        pass

    @abstractmethod
    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Any:
        # Simplification for MVP: Gemini-pro tool calling requires specific formatting
        # For now, we'll convert the messages and handle response
        chat = self.model.start_chat(history=[])
        # Last message is the current prompt
        prompt = messages[-1]["content"]
        response = await asyncio.to_thread(chat.send_message, prompt)
        return response.text

    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        chat = self.model.start_chat(history=[])
        prompt = messages[-1]["content"]
        response = await asyncio.to_thread(chat.send_message, prompt, stream=True)
        for chunk in response:
            yield chunk.text

class LLMClient:
    def __init__(self):
        self.provider: Optional[LLMProvider] = None
        if settings.GEMINI_API_KEY:
            self.provider = GeminiProvider(settings.GEMINI_API_KEY)
        elif settings.OPENAI_API_KEY:
            # Placeholder for OpenAI
            pass

    async def chat(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None):
        if not self.provider:
            return "Error: No LLM provider configured. Please set GEMINI_API_KEY or OPENAI_API_KEY."
        return await self.provider.chat_completion(messages, tools)

import asyncio # Needed for to_thread in MVP
llm_client = LLMClient()
