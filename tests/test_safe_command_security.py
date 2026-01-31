import pytest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
from troubleshooting_mcp.models import SafeCommandInput
from troubleshooting_mcp.tools import safe_command

@pytest.mark.asyncio
async def test_safe_command_security_argument_blocking():
    """
    Verify that dangerous arguments are blocked.
    """

    # Setup
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

    # Test case 1: ping -f (flood) - Should be blocked
    # Note: Validation happens at Pydantic model initialization
    with pytest.raises(ValidationError) as excinfo:
        params = SafeCommandInput(command="ping", args=["-f", "google.com"])
    assert "Argument '-f' is not allowed for command 'ping'" in str(excinfo.value)

    # Also test combined flags/prefixes if applicable
    with pytest.raises(ValidationError) as excinfo:
        params = SafeCommandInput(command="ping", args=["-flood", "google.com"])
    assert "Argument '-flood' is not allowed" in str(excinfo.value)

    # Test case 2: lsof -b
    with pytest.raises(ValidationError) as excinfo:
        params = SafeCommandInput(command="lsof", args=["-b", "/tmp"])
    assert "Argument '-b' is not allowed" in str(excinfo.value)

    # Test case 3: Safe command should still work
    params = SafeCommandInput(command="ping", args=["-c", "1", "google.com"])
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "ping output"
        mock_run.return_value.returncode = 0
        await func(params)
        assert mock_run.called
