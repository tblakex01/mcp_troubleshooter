
import pytest
import shutil
from unittest.mock import MagicMock
from troubleshooting_mcp.models import SafeCommandInput
from troubleshooting_mcp.tools import safe_command

@pytest.mark.asyncio
async def test_safe_command_argument_validation():
    """Test safe_command argument blocking."""
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

    # Mock shutil.which to ensure commands are "found"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(shutil, "which", lambda cmd: f"/usr/bin/{cmd}")

        # Test: dig -f (Blocked)
        params = SafeCommandInput(command="dig", args=["-f", "somefile"])
        result = await func(params)
        assert "Error: Security violation" in result
        assert "Argument '-f' is not allowed" in result

        # Test: dig with allowed arg (Should execute - or try to)
        # We need to mock subprocess.run to avoid actual execution failure/side effects
        with mp.context() as mp2:
            mock_run = MagicMock()
            mock_run.returncode = 0
            mock_run.stdout = "Mock output"
            mock_run.stderr = ""
            mp2.setattr("subprocess.run", lambda *args, **kwargs: mock_run)

            params = SafeCommandInput(command="dig", args=["google.com"])
            result = await func(params)
            assert "Mock output" in result

        # Test: lsof -F (Blocked)
        params = SafeCommandInput(command="lsof", args=["-F"])
        result = await func(params)
        assert "Error: Security violation" in result

        # Test: ss -K (Blocked)
        params = SafeCommandInput(command="ss", args=["-K"])
        result = await func(params)
        assert "Error: Security violation" in result

        # Test: ip netns (Blocked)
        params = SafeCommandInput(command="ip", args=["netns", "add", "bad"])
        result = await func(params)
        assert "Error: Security violation" in result

        # Test: ping -f (Blocked)
        params = SafeCommandInput(command="ping", args=["-f", "localhost"])
        result = await func(params)
        assert "Error: Security violation" in result

        # Test prefix matching: dig -ffile (Blocked)
        # Assuming -f is the blocked flag.
        # If I blocked "-f", then "-ffile" should also be blocked if the code checks starts_with.
        # My implementation does: if arg == blocked or arg.startswith(blocked)
        params = SafeCommandInput(command="dig", args=["-ffile"])
        result = await func(params)
        assert "Error: Security violation" in result

        # Test combined short flags: ping -cf (Blocked because -f is blocked)
        params = SafeCommandInput(command="ping", args=["-cf", "2", "localhost"])
        result = await func(params)
        assert "Error: Security violation" in result
        assert "contains blocked flag" in result

        # Test combined short flags safely: ls -la (Allowed)
        # We need a command that has blocked flags to test.
        # ss blocks -K. ss -tK should be blocked.
        params = SafeCommandInput(command="ss", args=["-tK"])
        result = await func(params)
        assert "Error: Security violation" in result
