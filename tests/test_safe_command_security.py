
import pytest
from unittest.mock import patch, MagicMock
from troubleshooting_mcp.tools.safe_command import register_safe_command
from troubleshooting_mcp.models import SafeCommandInput

class MockMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, name, annotations=None):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

@pytest.fixture
def mcp_tool():
    mcp = MockMCP()
    register_safe_command(mcp)
    return mcp.tools["troubleshooting_execute_safe_command"]

@pytest.mark.asyncio
async def test_safe_command_ip_netns_blocked(mcp_tool):
    """Test that 'ip netns' and 'ip -b' are blocked."""

    # Test ip netns
    params = SafeCommandInput(command="ip", args=["netns", "exec", "test", "ls"])
    result = await mcp_tool(params)
    assert "Error: Security violation" in result
    assert "netns" in result

    # Test ip -b (batch mode)
    params = SafeCommandInput(command="ip", args=["-b", "batchfile"])
    result = await mcp_tool(params)
    assert "Error: Security violation" in result
    # The error message includes the specific argument that triggered it
    assert "-b" in result

@pytest.mark.asyncio
async def test_safe_command_allowed_args(mcp_tool):
    """Test that safe ip commands are still allowed."""

    # We mock shutil.which and subprocess.run to avoid actual execution
    with patch("shutil.which", return_value="/usr/bin/ip"), \
         patch("subprocess.run") as mock_run:

        mock_run.return_value = MagicMock(
            stdout="127.0.0.1",
            stderr="",
            returncode=0
        )

        params = SafeCommandInput(command="ip", args=["addr", "show"])
        result = await mcp_tool(params)

        # Should not contain security error
        assert "Error: Security violation" not in result
        assert "Standard Output" in result
