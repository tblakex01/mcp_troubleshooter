
import pytest
from pydantic import ValidationError
from src.troubleshooting_mcp.models import SafeCommandInput

def test_safe_command_valid():
    """Test that valid commands are accepted."""
    input_data = SafeCommandInput(command="ping", args=["google.com", "-c", "4"])
    assert input_data.command == "ping"
    assert input_data.args == ["google.com", "-c", "4"]

def test_safe_command_blocked_flag_exact():
    """Test that blocked flags are rejected (exact match)."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="dig", args=["-f", "secret.txt"])

    assert "Argument '-f' is not allowed for command 'dig'" in str(excinfo.value)

def test_safe_command_blocked_flag_prefix():
    """Test that blocked flags are rejected (prefix match)."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="dig", args=["-fsecret.txt"])

    assert "Argument '-fsecret.txt' is not allowed for command 'dig'" in str(excinfo.value)

def test_safe_command_allowed_flag():
    """Test that allowed flags are accepted."""
    input_data = SafeCommandInput(command="dig", args=["google.com", "MX"])
    assert input_data.command == "dig"

def test_safe_command_ping_flood_blocked():
    """Test that ping flood is blocked."""
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ping", args=["-f", "google.com"])

    assert "Argument '-f' is not allowed for command 'ping'" in str(excinfo.value)

def test_safe_command_unknown_command_not_affected():
    """Test that commands without blocklist entries work normally."""
    # Assuming 'lsblk' has no blocked args in our list
    input_data = SafeCommandInput(command="lsblk", args=["-a"])
    assert input_data.command == "lsblk"
