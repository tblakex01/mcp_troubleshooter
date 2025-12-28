"""
Test security restrictions for SafeCommandInput.
"""

import pytest
from pydantic import ValidationError
from src.troubleshooting_mcp.models import SafeCommandInput

def test_ip_command_restrictions():
    """Test that dangerous arguments for 'ip' command are blocked."""

    # These should fail
    dangerous_args = [
        ["netns", "exec", "ls"],
        ["exec"],
        ["netns", "list"], # netns itself is blocked
    ]

    for args in dangerous_args:
        with pytest.raises(ValidationError) as excinfo:
            SafeCommandInput(command="ip", args=args)
        assert "Argument" in str(excinfo.value)
        assert "is not allowed for command 'ip'" in str(excinfo.value)

    # These should pass
    safe_args = [
        ["addr", "show"],
        ["link", "show"],
        ["route"],
        [],
    ]
    for args in safe_args:
        SafeCommandInput(command="ip", args=args)

def test_shell_injection_prevention():
    """Test that shell metacharacters are blocked in arguments."""

    forbidden_chars = [";", "&", "|", "`", "$", "(", ")", ">", "<", "{", "}", "!"]

    for char in forbidden_chars:
        with pytest.raises(ValidationError) as excinfo:
            SafeCommandInput(command="ping", args=["google.com", char, "ls"])
        assert f"Argument contains forbidden character '{char}'" in str(excinfo.value)

    # Test hidden in a string
    with pytest.raises(ValidationError):
        SafeCommandInput(command="ping", args=[f"google.com{char}ls"])

def test_normal_usage():
    """Test that normal usage is not affected."""

    valid_inputs = [
        ("ping", ["-c", "4", "google.com"]),
        ("lsblk", ["-f"]),
        ("free", ["-h"]),
        ("df", ["-h", "/"]),
    ]

    for cmd, args in valid_inputs:
        model = SafeCommandInput(command=cmd, args=args)
        assert model.command == cmd
        assert model.args == args
