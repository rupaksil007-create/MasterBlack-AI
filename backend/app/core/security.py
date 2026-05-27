import os
from pathlib import Path
from backend.app.core.config import settings

def validate_path(path: str, session_id: str) -> str:
    """
    Validates that a path is within the session's workspace.
    Returns the absolute path if valid, raises ValueError otherwise.
    """
    workspace_root = Path(settings.WORKSPACE_ROOT).resolve() / session_id
    requested_path = (workspace_root / path).resolve()

    if not str(requested_path).startswith(str(workspace_root)):
        raise ValueError(f"Access denied: Path {path} is outside the workspace root.")
    
    return str(requested_path)
