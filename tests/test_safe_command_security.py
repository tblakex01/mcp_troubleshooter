import pytest
from pydantic import ValidationError

try:
    from troubleshooting_mcp.models import SafeCommandInput
except ImportError:
    from src.troubleshooting_mcp.models import SafeCommandInput

def test_safe_command_argument_blocking():
    """Test that dangerous arguments are blocked."""

    # ip netns (Network Namespace execution)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ip", args=["netns", "exec", "foo"])

    # ip -n (Short for netns)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ip", args=["-n", "foo"])

    # ip -batch (Batch execution from file)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ip", args=["-batch", "/tmp/commands"])

    # dig -f (Batch mode from file)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="dig", args=["-f", "/etc/passwd"])

    # ping -f (Flood)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ping", args=["-f", "localhost"])

    # lsof +D (Recursive directory search - denial of service risk)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="lsof", args=["+D", "/"])

    # Valid commands should still work
    SafeCommandInput(command="ping", args=["-c", "4", "google.com"])
    SafeCommandInput(command="ip", args=["addr", "show"])
