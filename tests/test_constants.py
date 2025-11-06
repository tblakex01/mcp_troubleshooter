"""
Tests for constants module.
"""

from troubleshooting_mcp.constants import (
    CHARACTER_LIMIT,
    COMMON_LOG_PATHS,
    SAFE_COMMANDS,
)


def test_character_limit_is_positive():
    """Test that CHARACTER_LIMIT is a positive integer."""
    assert isinstance(CHARACTER_LIMIT, int)
    assert CHARACTER_LIMIT > 0
    assert CHARACTER_LIMIT == 25000


def test_safe_commands_is_set():
    """Test that SAFE_COMMANDS is a set."""
    assert isinstance(SAFE_COMMANDS, set)
    assert len(SAFE_COMMANDS) > 0


def test_safe_commands_contains_basic_commands():
    """Test that SAFE_COMMANDS contains expected basic commands."""
    expected_commands = {"ping", "df", "uptime", "whoami", "hostname"}
    assert expected_commands.issubset(SAFE_COMMANDS)


def test_safe_commands_no_dangerous_commands():
    """Test that SAFE_COMMANDS doesn't contain dangerous commands."""
    dangerous_commands = {"rm", "dd", "mkfs", "chmod", "chown", "kill", "sudo"}
    assert not dangerous_commands.intersection(SAFE_COMMANDS)


def test_common_log_paths_is_list():
    """Test that COMMON_LOG_PATHS is a list."""
    assert isinstance(COMMON_LOG_PATHS, list)
    assert len(COMMON_LOG_PATHS) > 0


def test_common_log_paths_contains_expected_paths():
    """Test that COMMON_LOG_PATHS contains some expected log paths."""
    # At least one of these should be present
    expected_paths = ["/var/log/syslog", "/var/log/messages"]
    assert any(path in COMMON_LOG_PATHS for path in expected_paths)
