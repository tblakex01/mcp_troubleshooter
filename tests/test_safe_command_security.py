
import pytest
import shutil
from src.troubleshooting_mcp.tools.safe_command import register_safe_command
from src.troubleshooting_mcp.models import SafeCommandInput

# Mock mcp object
class MockMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, name, annotations):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

@pytest.fixture
def mcp():
    return MockMCP()

@pytest.fixture
def safe_command_tool(mcp):
    register_safe_command(mcp)
    return mcp.tools["troubleshooting_execute_safe_command"]

@pytest.mark.asyncio
async def test_blocked_arguments(safe_command_tool):
    """Test that blocked arguments are rejected."""

    # Test dig -f (blocked)
    result = await safe_command_tool(
        SafeCommandInput(command="dig", args=["-f", "somefile"])
    )
    assert "Error: Argument '-f' is not allowed" in result

    # Test dig -af (blocked because of -f)
    result = await safe_command_tool(
        SafeCommandInput(command="dig", args=["-af", "somefile"])
    )
    assert "Error: Argument '-f' is not allowed" in result

    # Test ip netns (blocked)
    result = await safe_command_tool(
        SafeCommandInput(command="ip", args=["netns", "list"])
    )
    assert "Error: Argument 'netns' is not allowed" in result

    # Test allowed command
    if shutil.which("ping"):
        # We assume ping is available and safe
        # Use a short timeout to avoid waiting too long
        result = await safe_command_tool(
            SafeCommandInput(command="ping", args=["-c", "1", "127.0.0.1"], timeout=1)
        )
        assert "Error: Argument" not in result
        assert "Command Execution: ping" in result

@pytest.mark.asyncio
async def test_lsof_blocked(safe_command_tool):
    """Test blocking of lsof -F."""
    result = await safe_command_tool(
        SafeCommandInput(command="lsof", args=["-F"])
    )
    assert "Error: Argument '-F' is not allowed" in result

@pytest.mark.asyncio
async def test_ss_blocked(safe_command_tool):
    """Test blocking of ss -K."""
    result = await safe_command_tool(
        SafeCommandInput(command="ss", args=["-K"])
    )
    assert "Error: Argument '-K' is not allowed" in result
