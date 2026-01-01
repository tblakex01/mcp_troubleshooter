
import pytest
from unittest.mock import MagicMock, patch
from troubleshooting_mcp.models import SafeCommandInput
from troubleshooting_mcp.tools import safe_command

@pytest.mark.asyncio
async def test_safe_command_ip_security_block():
    """Test that safe_command blocks dangerous ip arguments."""
    mcp = MagicMock()
    tool_funcs = []
    def mock_tool(*args, **kwargs):
        def decorator(func):
            tool_funcs.append(func)
            return func
        return decorator
    mcp.tool = mock_tool
    safe_command.register_safe_command(mcp)
    func = tool_funcs[0]

    # Test blocking 'netns'
    params = SafeCommandInput(command="ip", args=["netns", "exec", "sh"])
    with patch("shutil.which", return_value="/usr/bin/ip"):
        result = await func(params)
        assert "Error: Argument 'netns' is not allowed" in result

    # Test blocking 'net' (abbreviation)
    params = SafeCommandInput(command="ip", args=["net"])
    with patch("shutil.which", return_value="/usr/bin/ip"):
        result = await func(params)
        assert "Error: Argument 'net' is not allowed" in result

    # Test blocking '-batch'
    params = SafeCommandInput(command="ip", args=["-batch", "file"])
    with patch("shutil.which", return_value="/usr/bin/ip"):
        result = await func(params)
        assert "Error: Argument '-batch' is not allowed" in result

@pytest.mark.asyncio
async def test_safe_command_dig_security_block():
    """Test that safe_command blocks dangerous dig arguments."""
    mcp = MagicMock()
    tool_funcs = []
    def mock_tool(*args, **kwargs):
        def decorator(func):
            tool_funcs.append(func)
            return func
        return decorator
    mcp.tool = mock_tool
    safe_command.register_safe_command(mcp)
    func = tool_funcs[0]

    # Test blocking '-f'
    params = SafeCommandInput(command="dig", args=["-f", "/etc/passwd"])
    with patch("shutil.which", return_value="/usr/bin/dig"):
        result = await func(params)
        assert "Error: Argument '-f' is not allowed" in result
