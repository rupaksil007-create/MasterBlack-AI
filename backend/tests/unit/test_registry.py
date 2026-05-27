import pytest
from backend.app.tools.registry import tool_registry

@pytest.mark.asyncio
async def test_registry_list_tools():
    tools = tool_registry.list_tools()
    assert len(tools) >= 3
    names = [t["name"] for t in tools]
    assert "bash_execute" in names
    assert "read_file" in names
    assert "write_file" in names

@pytest.mark.asyncio
async def test_registry_get_tool():
    tool = tool_registry.get_tool("bash_execute")
    assert tool is not None
    assert tool.name == "bash_execute"

@pytest.mark.asyncio
async def test_registry_call_nonexistent():
    with pytest.raises(ValueError, match="Tool not found"):
        await tool_registry.call_tool("ghost_tool", "session-1")
