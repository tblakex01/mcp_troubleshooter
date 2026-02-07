import pytest
from pydantic import ValidationError
try:
    from troubleshooting_mcp.models import SafeCommandInput
except ImportError:
    from src.troubleshooting_mcp.models import SafeCommandInput

def test_dig_file_read_blocked():
    """Test that dig -f is blocked."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="dig", args=["-f", "/etc/passwd"])
    assert "Argument '-f' is not allowed for command 'dig'" in str(excinfo.value)
    assert "Blocked prefix: '-f'" in str(excinfo.value)

def test_dig_file_read_prefix_blocked():
    """Test that dig -ffile is blocked (prefix match)."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="dig", args=["-ffile"])
    assert "Argument '-ffile' is not allowed for command 'dig'" in str(excinfo.value)

def test_ping_flood_blocked():
    """Test that ping -f is blocked."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ping", args=["-f"])
    assert "Argument '-f' is not allowed for command 'ping'" in str(excinfo.value)

def test_ping_flood_prefix_blocked():
    """Test that ping -f is blocked even if stuck to other chars."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ping", args=["-flood"])
    assert "Argument '-flood' is not allowed for command 'ping'" in str(excinfo.value)

def test_valid_dig_allowed():
    """Test that valid dig commands are allowed."""
    input_model = SafeCommandInput(command="dig", args=["google.com"])
    assert input_model.command == "dig"
    assert input_model.args == ["google.com"]

def test_valid_ping_allowed():
    """Test that valid ping commands are allowed."""
    input_model = SafeCommandInput(command="ping", args=["-c", "4", "google.com"])
    assert input_model.command == "ping"
    assert input_model.args == ["-c", "4", "google.com"]

def test_other_command_allowed():
    """Test that commands without blocklist are not affected."""
    input_model = SafeCommandInput(command="uptime", args=[])
    assert input_model.command == "uptime"

def test_case_insensitive_command():
    """Test that command matching is case insensitive."""
    # "DIG" should match "dig" blocklist
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="DIG", args=["-f", "file"])
    assert "Argument '-f' is not allowed for command 'dig'" in str(excinfo.value)
