
import pytest
from pydantic import ValidationError
from troubleshooting_mcp.models import SafeCommandInput

def test_safe_command_input_valid_args():
    """Test that valid arguments are accepted."""
    valid_inputs = [
        [],
        ["-a"],
        ["-l", "/var/log"],
        ["--verbose"],
        ["user@host.com"],
        ["192.168.1.1"],
        ["/path/to/file.txt"],
        ["file_name-1.2.3"]
    ]

    for args in valid_inputs:
        model = SafeCommandInput(command="lsblk", args=args)
        assert model.args == args

def test_safe_command_input_invalid_args():
    """Test that arguments with dangerous characters are rejected."""
    invalid_inputs = [
        [";"],
        ["|"],
        ["&&"],
        ["$HOME"],
        ["`ls`"],
        ["$(ls)"],
        [">"],
        ["<"],
        ["file*"],  # wildcard
        ["test?"],  # wildcard
        ["(subshell)"],
        ["{brace,expansion}"],
        ["\\"],     # backslash
        ["'quote'"],
        ['"doublequote"']
    ]

    for args in invalid_inputs:
        with pytest.raises(ValidationError) as excinfo:
            SafeCommandInput(command="lsblk", args=args)
        assert "Invalid argument" in str(excinfo.value)
        assert "Arguments must only contain" in str(excinfo.value)

def test_safe_command_input_command_validation():
    """Test that command validation still works."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="rm", args=["-rf", "/"])
    assert "Command 'rm' is not in the whitelist" in str(excinfo.value)
