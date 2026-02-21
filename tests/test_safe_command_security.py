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

def test_safe_command_additional_blocks():
    """Test blocking of dangerous arguments for ss, du, and hostname."""

    # ss -D (Arbitrary file overwrite)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["-D", "/tmp/pwned.txt"])

    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["--diag", "/tmp/pwned.txt"])

    # ss -F (Arbitrary file read)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["-F", "/etc/passwd"])

    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["--filter", "/etc/passwd"])

    # ss -K (Destructive - kill sockets)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["-K"])

    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["--kill"])

    # ss -N (Namespace switching)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["-N", "testns"])

    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="ss", args=["--net", "testns"])

    # du --files0-from (Arbitrary file read via error message)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="du", args=["--files0-from", "/etc/shadow"])

    # hostname -F (Set hostname from file / Read file content via hostname)
    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="hostname", args=["-F", "/etc/passwd"])

    with pytest.raises(ValidationError, match="Argument .* is not allowed"):
        SafeCommandInput(command="hostname", args=["--file", "/etc/passwd"])

    # Valid commands should still work
    SafeCommandInput(command="ss", args=["-t", "-a"])
    SafeCommandInput(command="du", args=["-h", "/var/log"])
    SafeCommandInput(command="hostname", args=[])
