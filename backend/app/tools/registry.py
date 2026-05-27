import logging
from typing import Dict, List, Any, Optional
from backend.app.tools.base import Tool
from backend.app.tools.editor import ReadFileTool, WriteFileTool
from backend.app.tools.bash import BashTool

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self.register_tool(ReadFileTool())
        self.register_tool(WriteFileTool())
        self.register_tool(BashTool())

    def register_tool(self, tool: Tool):
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema
            }
            for tool in self._tools.values()
        ]

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns tool definitions in OpenAI function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema
                }
            }
            for tool in self._tools.values()
        ]

    async def call_tool(self, name: str, session_id: str, **kwargs) -> Any:
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        logger.info(f"Calling tool {name} for session {session_id}")
        return await tool.execute(session_id, **kwargs)

tool_registry = ToolRegistry()
