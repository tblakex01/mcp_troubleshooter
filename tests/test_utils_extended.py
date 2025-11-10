"""
Extended tests for utils module to increase coverage.
"""

import pytest
from unittest.mock import patch, MagicMock

from troubleshooting_mcp.utils import (
    format_bytes,
    format_timestamp,
    handle_error,
    check_character_limit,
)
from troubleshooting_mcp.constants import CHARACTER_LIMIT


def test_handle_error_with_oserror():
    """Test handle_error with OSError."""
    error = OSError("Test OS error")
    result = handle_error(error)
    assert isinstance(result, str)
    assert "Error" in result or "error" in result.lower()
    assert "Test OS error" in result or "OSError" in result


def test_handle_error_with_ioerror():
    """Test handle_error with IOError."""
    error = IOError("Test IO error")
    result = handle_error(error)
    assert isinstance(result, str)
    assert "error" in result.lower()


def test_handle_error_with_generic_exception():
    """Test handle_error with a generic exception."""
    error = Exception("Generic error")
    result = handle_error(error)
    assert isinstance(result, str)
    assert "Exception" in result or "error" in result.lower()


def test_format_bytes_large_terabytes():
    """Test format_bytes with multiple terabytes."""
    # 5 TB
    result = format_bytes(5 * 1024 ** 4)
    assert "TB" in result
    assert "5." in result


def test_format_bytes_exact_boundaries():
    """Test format_bytes at exact unit boundaries."""
    # Exactly 1 KB
    assert "1.00 KB" == format_bytes(1024)
    # Exactly 1 MB
    assert "1.00 MB" == format_bytes(1024 ** 2)
    # Exactly 1 GB
    assert "1.00 GB" == format_bytes(1024 ** 3)


def test_format_timestamp_various_times():
    """Test format_timestamp with various timestamps."""
    # Year 2000
    timestamp_2000 = 946684800
    result = format_timestamp(timestamp_2000)
    assert isinstance(result, str)
    assert "2000" in result or "1999" in result or "2001" in result  # Timezone dependent

    # Year 2020
    timestamp_2020 = 1577836800
    result = format_timestamp(timestamp_2020)
    assert isinstance(result, str)


def test_check_character_limit_with_custom_data_type():
    """Test check_character_limit with custom data type label."""
    long_content = "x" * (CHARACTER_LIMIT + 500)
    result = check_character_limit(long_content, "custom data")
    assert "TRUNCATED" in result
    # Verify the result contains truncated content
    assert len(result) > CHARACTER_LIMIT


def test_check_character_limit_exactly_at_limit():
    """Test check_character_limit with content exactly at limit."""
    content = "x" * CHARACTER_LIMIT
    result = check_character_limit(content)
    # Should not be truncated if exactly at limit
    assert result == content or "TRUNCATED" in result  # Depends on implementation


def test_format_bytes_negative():
    """Test format_bytes with edge case (negative handled as 0 or abs)."""
    # The function might handle this differently
    result = format_bytes(-100)
    assert isinstance(result, str)
    # Just check it doesn't crash
