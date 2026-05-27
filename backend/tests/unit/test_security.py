import pytest
from backend.app.core.security import validate_path
from backend.app.core.config import settings

def test_validate_path_valid():
    session_id = "test-session"
    path = "src/main.py"
    # Should not raise exception
    valid_path = validate_path(path, session_id)
    assert session_id in valid_path
    assert "src/main.py" in valid_path.replace("\\", "/")

def test_validate_path_traversal():
    session_id = "test-session"
    path = "../../../etc/passwd"
    with pytest.raises(ValueError, match="outside the workspace root"):
        validate_path(path, session_id)

def test_validate_path_absolute():
    session_id = "test-session"
    path = "/etc/passwd"
    # Even if path is absolute, our join logic usually treats it relative to base
    # but we should still check if it escapes.
    with pytest.raises(ValueError, match="outside the workspace root"):
        validate_path(path, session_id)
