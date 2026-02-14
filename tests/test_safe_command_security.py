import pytest
from pydantic import ValidationError
from src.troubleshooting_mcp.models import SafeCommandInput

def test_dig_security_block():
    """Test that dig -f is blocked."""
    with pytest.raises(ValidationError) as exc:
        SafeCommandInput(command="dig", args=["-f", "/etc/passwd"])
    assert "Argument '-f' is not allowed" in str(exc.value)

def test_dig_joined_flag_block():
    """Test that dig -f/etc/passwd is blocked."""
    with pytest.raises(ValidationError) as exc:
        SafeCommandInput(command="dig", args=["-f/etc/passwd"])
    assert "Arguments starting with '-f' are restricted" in str(exc.value)

def test_dig_safe_usage():
    """Test that dig with safe arguments is allowed."""
    input_data = SafeCommandInput(command="dig", args=["google.com", "A"])
    assert input_data.command == "dig"
    assert input_data.args == ["google.com", "A"]

def test_ip_batch_block():
    """Test that ip -b / -batch is blocked."""
    for bad_arg in ["-b", "-batch", "-bat", "-ba"]:
        with pytest.raises(ValidationError) as exc:
            SafeCommandInput(command="ip", args=[bad_arg, "/tmp/commands"])
        assert "Batch mode (-b, -batch) is restricted" in str(exc.value)

def test_ip_brief_allow():
    """Test that ip -br / -brief is allowed."""
    for good_arg in ["-br", "-brief", "-bri", "-brie"]:
        input_data = SafeCommandInput(command="ip", args=[good_arg, "address"])
        assert input_data.command == "ip"
        assert input_data.args == [good_arg, "address"]

def test_ss_dump_block():
    """Test that ss -D / --dump / -F / --filter are blocked."""
    for bad_arg in ["-D", "--dump", "-F", "--filter"]:
        with pytest.raises(ValidationError) as exc:
            SafeCommandInput(command="ss", args=[bad_arg, "/tmp/file"])
        # We check for substring because error message might be slightly different depending on which block triggered
        assert "restricted for security reasons" in str(exc.value)

def test_ss_safe_usage():
    """Test that ss -f inet (family) is allowed."""
    input_data = SafeCommandInput(command="ss", args=["-f", "inet"])
    assert input_data.args == ["-f", "inet"]

def test_ping_flood_block():
    """Test that ping -f is blocked."""
    with pytest.raises(ValidationError) as exc:
        SafeCommandInput(command="ping", args=["-f"])
    assert "Arguments starting with '-f' are restricted" in str(exc.value)

def test_ping_safe_usage():
    """Test that ping google.com is allowed."""
    input_data = SafeCommandInput(command="ping", args=["-c", "4", "google.com"])
    assert input_data.args == ["-c", "4", "google.com"]
