"""
Tests for security argument filtering in SafeCommandInput.
"""

import pytest
from pydantic import ValidationError
from troubleshooting_mcp.models import SafeCommandInput

class TestSecurityArgs:
    """Tests for ensuring dangerous arguments are blocked via allowlist."""

    def test_ip_netns_exec_blocked(self):
        """Test that 'ip netns exec' is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="ip", args=["netns", "exec", "foo", "ls"])
        assert "not allowed for ip command" in str(exc_info.value)

    def test_ip_abbrev_netns_blocked(self):
        """Test that 'ip net exec' (abbreviation) is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="ip", args=["net", "exec", "foo", "ls"])
        assert "not allowed for ip command" in str(exc_info.value)

    def test_ip_batch_blocked(self):
        """Test that 'ip -b' is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="ip", args=["-b", "script.txt"])
        assert "not allowed for ip command" in str(exc_info.value)

    def test_ip_abbrev_batch_blocked(self):
        """Test that 'ip -ba' is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="ip", args=["-ba", "script.txt"])
        assert "not allowed for ip command" in str(exc_info.value)

    def test_ip_addr_allowed(self):
        """Test that 'ip addr' is allowed."""
        model = SafeCommandInput(command="ip", args=["addr", "show"])
        assert model.args == ["addr", "show"]

    def test_ip_abbrev_a_allowed(self):
        """Test that 'ip a' is allowed."""
        model = SafeCommandInput(command="ip", args=["a"])
        assert model.args == ["a"]

    def test_ip_route_allowed(self):
        """Test that 'ip route' is allowed."""
        model = SafeCommandInput(command="ip", args=["route"])
        assert model.args == ["route"]

    def test_ip_unknown_object_blocked(self):
        """Test that unknown ip objects are blocked."""
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="ip", args=["unknown_object"])
        assert "not allowed for ip command" in str(exc_info.value)

    def test_other_command_args_allowed(self):
        """Test that other commands can take arbitrary args."""
        model = SafeCommandInput(command="lsblk", args=["-f"])
        assert model.args == ["-f"]
