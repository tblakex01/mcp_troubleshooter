
import pytest
import shutil
from src.troubleshooting_mcp.tools.safe_command import register_safe_command
from src.troubleshooting_mcp.models import SafeCommandInput

# Mock MCP class to simulate the server's decorator behavior
class MockMCP:
    def __init__(self):
        self.func = None

    def tool(self, name, annotations):
        def decorator(func):
            self.func = func
            return func
        return decorator

@pytest.mark.asyncio
async def test_safe_command_ip_security():
    """Test that potentially dangerous 'ip' command arguments are blocked."""
    mcp = MockMCP()
    register_safe_command(mcp)

    # Ensure tool was registered
    assert mcp.func is not None

    # Test blocked argument: set
    params = SafeCommandInput(
        command="ip",
        args=["link", "set", "eth0", "down"],
        timeout=5
    )
    result = await mcp.func(params)
    assert "Error: Security violation" in result
    assert "Argument 'set' is not allowed" in result

    # Test blocked argument: add
    params = SafeCommandInput(
        command="ip",
        args=["addr", "add", "192.168.1.1/24", "dev", "eth0"],
        timeout=5
    )
    result = await mcp.func(params)
    assert "Error: Security violation" in result
    assert "Argument 'add' is not allowed" in result

    # Test allowed argument: show (valid usage)
    # We rely on 'ip' command existence. If not present, we check for "Command not found"
    # But if present, it should NOT be a security violation.
    if shutil.which("ip"):
        params = SafeCommandInput(
            command="ip",
            args=["addr", "show"],
            timeout=5
        )
        result = await mcp.func(params)
        assert "Error: Security violation" not in result

@pytest.mark.asyncio
async def test_safe_command_ifconfig_security():
    """Test that potentially dangerous 'ifconfig' command arguments are blocked."""
    mcp = MockMCP()
    register_safe_command(mcp)

    # Test blocked argument: down
    params = SafeCommandInput(
        command="ifconfig",
        args=["eth0", "down"],
        timeout=5
    )
    result = await mcp.func(params)
    assert "Error: Security violation" in result
    assert "Argument 'down' is not allowed" in result

    # Test blocked argument: promisc
    params = SafeCommandInput(
        command="ifconfig",
        args=["eth0", "promisc"],
        timeout=5
    )
    result = await mcp.func(params)
    assert "Error: Security violation" in result
    assert "Argument 'promisc' is not allowed" in result

@pytest.mark.asyncio
async def test_safe_command_general_security():
    """Test generic security aspects."""
    mcp = MockMCP()
    register_safe_command(mcp)

    # Test command not in whitelist (handled by Pydantic, but double check)
    # Pydantic validation happens before tool execution usually, but here we call tool directly.
    # Wait, the Pydantic model throws error on init.
    try:
        SafeCommandInput(command="rm", args=["-rf", "/"])
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "not in the whitelist" in str(e)
