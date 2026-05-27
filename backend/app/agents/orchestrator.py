import logging
import asyncio
import json
from typing import Dict, Any, List, Optional
from backend.app.tools.registry import tool_registry
from backend.app.websockets.manager import manager
from backend.app.websockets.protocol import WebSocketMessage, EventType
from backend.app.services.llm_client import llm_client
from backend.app.memory.context_manager import get_context

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.is_running = False
        self.context = get_context(session_id)

    async def process_request(self, user_input: str):
        """
        Intelligent request lifecycle:
        1. Add user input to memory
        2. Enter Reasoning Loop:
           a. Query LLM with context and tools
           b. If LLM wants to talk -> stream to user
           c. If LLM wants tool -> execute tool -> add result to memory -> repeat
        """
        if self.is_running:
            await self._send_error("An agent is already running for this session.")
            return

        self.is_running = True
        self.context.add_message("user", user_input)
        
        try:
            # For MVP, we use a simple loop. 
            # Real-world implementations handle parallel tool calls and token limits.
            max_iterations = 10
            iterations = 0

            while iterations < max_iterations:
                iterations += 1
                
                # Get OpenAI-style tool definitions
                tools = tool_registry.get_tool_definitions()
                messages = self.context.get_messages_for_llm()

                # Add a system prompt to guide the reasoning
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are MasterBlack AI, a senior software engineer assistant. "
                        "You have access to a sandbox environment with tools for file editing and shell execution. "
                        "Work autonomously to solve the user's request. "
                        "If you need to see a file, read it. If you need to run code, use bash_execute. "
                        "Always explain your thoughts before taking action."
                    )
                }
                full_messages = [system_prompt] + messages

                # Call LLM (Simplified for MVP: Gemini-pro without native tool calling yet)
                # We'll simulate a tool-calling response format if the LLM outputs JSON
                await self._send_thought("Reasoning about next steps...")
                
                response_text = await llm_client.chat(full_messages, tools=tools)
                
                # Check for tool call pattern in response (MVP hack)
                # In production, this would use native LLM tool calling fields
                tool_call = self._parse_tool_call(response_text)
                
                if tool_call:
                    tool_name = tool_call["action"]
                    tool_args = tool_call["arguments"]
                    
                    await self._send_thought(f"I've decided to use {tool_name}")
                    result = await self._execute_tool(tool_name, **tool_args)
                    
                    # Add tool result to context
                    self.context.add_message("assistant", f"Executed {tool_name}", name=tool_name)
                    self.context.add_message("tool", json.dumps(result), name=tool_name)
                else:
                    # Final response
                    self.context.add_message("assistant", response_text)
                    await manager.send_message(WebSocketMessage(
                        type=EventType.LOG, # Using LOG for final text for now
                        session_id=self.session_id,
                        data={"level": "info", "message": response_text}
                    ))
                    break

        except Exception as e:
            logger.error(f"Error in intelligent orchestrator loop: {e}")
            await self._send_error(str(e))
        
        finally:
            self.is_running = False

    def _parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """Parses a JSON tool call from LLM text (MVP implementation)."""
        try:
            # Look for ```json ... ``` or raw JSON
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
                if "action" in data and "arguments" in data:
                    return data
            
            # Try raw JSON if no block found
            data = json.loads(text)
            if "action" in data and "arguments" in data:
                return data
        except:
            pass
        return None

    async def _execute_tool(self, tool_name: str, **kwargs):
        await manager.send_message(WebSocketMessage(
            type=EventType.TOOL_START,
            session_id=self.session_id,
            data={"tool_name": tool_name, "parameters": kwargs}
        ))

        result = await tool_registry.call_tool(tool_name, self.session_id, **kwargs)

        await manager.send_message(WebSocketMessage(
            type=EventType.TOOL_RESULT,
            session_id=self.session_id,
            data={"tool_name": tool_name, "result": result, "success": "error" not in result}
        ))
        return result

    async def _send_thought(self, thought: str):
        await manager.send_message(WebSocketMessage(
            type=EventType.AGENT_THOUGHT,
            session_id=self.session_id,
            data={"thought": thought}
        ))

    async def _send_error(self, error: str):
        await manager.send_message(WebSocketMessage(
            type=EventType.ERROR,
            session_id=self.session_id,
            data={"message": error}
        ))

# Session-to-Orchestrator mapping
orchestrators: Dict[str, Orchestrator] = {}

def get_orchestrator(session_id: str) -> Orchestrator:
    if session_id not in orchestrators:
        orchestrators[session_id] = Orchestrator(session_id)
    return orchestrators[session_id]
