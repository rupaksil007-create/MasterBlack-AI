import os
from typing import Any, Dict
from backend.app.tools.base import Tool
from backend.app.core.security import validate_path
from backend.app.sandbox.docker_manager import sandbox_manager

class ReadFileTool(Tool):
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Reads the content of a file from the sandbox workspace."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the file."}
            },
            "required": ["path"]
        }

    async def execute(self, session_id: str, **kwargs) -> Any:
        path = kwargs.get("path")
        if not path:
            return {"error": "Path is required"}
        
        # In a real implementation, we'd use container.get_archive or exec cat
        # For MVP, we use the fact that the workspace is mounted on the host
        try:
            full_path = validate_path(path, session_id)
            if not os.path.exists(full_path):
                return {"error": f"File not found: {path}"}
            
            with open(full_path, "r") as f:
                return {"content": f.read()}
        except Exception as e:
            return {"error": str(e)}

class WriteFileTool(Tool):
    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Writes content to a file in the sandbox workspace."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path to the file."},
                "content": {"type": "string", "description": "Content to write."}
            },
            "required": ["path", "content"]
        }

    async def execute(self, session_id: str, **kwargs) -> Any:
        path = kwargs.get("path")
        content = kwargs.get("content")
        
        try:
            full_path = validate_path(path, session_id)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w") as f:
                f.write(content)
            return {"success": True, "path": path}
        except Exception as e:
            return {"error": str(e)}
