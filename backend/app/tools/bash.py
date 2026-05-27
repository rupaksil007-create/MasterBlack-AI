from typing import Any, Dict
from backend.app.tools.base import Tool
from backend.app.sandbox.docker_manager import sandbox_manager

class BashTool(Tool):
    @property
    def name(self) -> str:
        return "bash_execute"

    @property
    def description(self) -> str:
        return "Executes a bash command in the isolated sandbox environment."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute."}
            },
            "required": ["command"]
        }

    async def execute(self, session_id: str, **kwargs) -> Any:
        command = kwargs.get("command")
        if not command:
            return {"error": "Command is required"}
        
        # We need a way to get the container_id for the session.
        # For now, we'll recreate or find it based on session_id
        container_id = sandbox_manager.create_sandbox(session_id)
        if not container_id:
            return {"error": "Failed to access sandbox"}

        result = sandbox_manager.execute_command(container_id, command)
        return result
