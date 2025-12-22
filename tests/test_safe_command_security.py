
import pytest
from unittest.mock import MagicMock, patch
from troubleshooting_mcp.models import SafeCommandInput
from troubleshooting_mcp.tools import safe_command

class TestSafeCommandSecurity:

    @pytest.fixture
    def safe_cmd_func(self):
        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        safe_command.register_safe_command(mcp)
        return tool_funcs[0]

    @pytest.mark.asyncio
    async def test_block_ip_modification(self, safe_cmd_func):
        """Test that 'ip' command blocks modification arguments."""
        # dangerous: ip link set eth0 down
        params = SafeCommandInput(command="ip", args=["link", "set", "eth0", "down"])

        with patch("subprocess.run") as mock_run:
            result = await safe_cmd_func(params)

            # Use 'or' to allow the test to pass if I fix it, fail if I haven't
            if mock_run.called:
                pytest.fail(f"Vulnerability: 'ip link set' was executed. Result: {result}")

            assert "Security violation" in result or "not allowed" in result

    @pytest.mark.asyncio
    async def test_block_ifconfig_modification(self, safe_cmd_func):
        """Test that 'ifconfig' command blocks modification arguments."""
        # dangerous: ifconfig eth0 down
        params = SafeCommandInput(command="ifconfig", args=["eth0", "down"])

        with patch("subprocess.run") as mock_run:
            result = await safe_cmd_func(params)

            if mock_run.called:
                pytest.fail(f"Vulnerability: 'ifconfig down' was executed. Result: {result}")

            assert "Security violation" in result or "not allowed" in result

    @pytest.mark.asyncio
    async def test_block_hostname_set(self, safe_cmd_func):
        """Test that 'hostname' command blocks setting new hostname."""
        # dangerous: hostname newname
        params = SafeCommandInput(command="hostname", args=["newname"])

        with patch("subprocess.run") as mock_run:
            result = await safe_cmd_func(params)

            if mock_run.called:
                pytest.fail(f"Vulnerability: 'hostname newname' was executed. Result: {result}")

            assert "Security violation" in result or "not allowed" in result

    @pytest.mark.asyncio
    async def test_allow_safe_ip_command(self, safe_cmd_func):
        """Test that safe 'ip' commands are still allowed."""
        params = SafeCommandInput(command="ip", args=["addr", "show"])

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "127.0.0.1"
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0

            result = await safe_cmd_func(params)

            assert mock_run.called
            assert "127.0.0.1" in result
