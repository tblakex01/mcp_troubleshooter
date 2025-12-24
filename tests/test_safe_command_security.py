"""
Security tests for safe_command tool.
"""

from unittest.mock import MagicMock, patch
import pytest
from troubleshooting_mcp.models import SafeCommandInput

class TestSafeCommandSecurity:
    """Security tests for safe_command tool."""

    @pytest.mark.asyncio
    async def test_safe_command_blocks_ip_netns(self):
        """Test that ip netns is blocked."""
        from troubleshooting_mcp.tools import safe_command

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

        # Test ip netns exec
        params = SafeCommandInput(command="ip", args=["netns", "exec", "test", "ls"])

        # We mock subprocess.run to avoid actual execution,
        # but we mainly want to see if the function checks args BEFORE calling subprocess.
        with patch("subprocess.run") as mock_run:
            result = await func(params)

            # IF vulnerable, it attempts to run the command, so mock_run is called.
            # IF secure, it returns an error before calling mock_run.

            # The test expects the code to be SECURE, so it asserts that
            # the result contains a security error and mock_run was NOT called.

            if mock_run.called:
                pytest.fail("Security vulnerability: 'ip netns' was executed via subprocess!")

            assert "Security violation" in result or "not allowed" in result

    @pytest.mark.asyncio
    async def test_safe_command_blocks_ip_batch(self):
        """Test that ip -b (batch) is blocked."""
        from troubleshooting_mcp.tools import safe_command

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

        # Test ip -b
        params = SafeCommandInput(command="ip", args=["-b", "commands.txt"])

        with patch("subprocess.run") as mock_run:
            result = await func(params)

            if mock_run.called:
                pytest.fail("Security vulnerability: 'ip -b' was executed via subprocess!")

            assert "Security violation" in result or "not allowed" in result
