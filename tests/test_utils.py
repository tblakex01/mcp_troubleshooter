"""
Tests for utility functions.
"""

from troubleshooting_mcp.constants import CHARACTER_LIMIT
from troubleshooting_mcp.utils import (
    check_character_limit,
    format_bytes,
    format_timestamp,
    handle_error,
)


class TestFormatBytes:
    """Tests for format_bytes function."""

    def test_bytes(self):
        assert format_bytes(500) == "500.00 B"

    def test_kilobytes(self):
        assert format_bytes(2048) == "2.00 KB"

    def test_megabytes(self):
        assert format_bytes(1048576) == "1.00 MB"

    def test_gigabytes(self):
        assert format_bytes(1073741824) == "1.00 GB"

    def test_terabytes(self):
        assert format_bytes(1099511627776) == "1.00 TB"

    def test_zero_bytes(self):
        assert format_bytes(0) == "0.00 B"


class TestFormatTimestamp:
    """Tests for format_timestamp function."""

    def test_unix_timestamp(self):
        # Unix epoch
        result = format_timestamp(0)
        # Result depends on timezone, but should be a valid date string
        assert len(result) > 0
        assert "-" in result
        assert ":" in result

    def test_recent_timestamp(self):
        # 2025-01-01 00:00:00 UTC
        timestamp = 1735689600
        result = format_timestamp(timestamp)
        assert "2025" in result or "2024" in result  # Timezone dependent


class TestHandleError:
    """Tests for handle_error function."""

    def test_permission_error(self):
        error = PermissionError("Access denied")
        result = handle_error(error)
        assert "Permission denied" in result
        assert "elevated privileges" in result

    def test_file_not_found_error(self):
        error = FileNotFoundError("File missing")
        result = handle_error(error)
        assert "File or resource not found" in result

    def test_timeout_error(self):
        error = TimeoutError("Operation timed out")
        result = handle_error(error)
        assert "Operation timed out" in result

    def test_value_error(self):
        error = ValueError("Invalid value")
        result = handle_error(error)
        assert "Invalid input" in result
        assert "Invalid value" in result

    def test_generic_exception(self):
        error = RuntimeError("Something went wrong")
        result = handle_error(error)
        assert "RuntimeError" in result
        assert "Something went wrong" in result


class TestCheckCharacterLimit:
    """Tests for check_character_limit function."""

    def test_content_within_limit(self):
        content = "Short content"
        result = check_character_limit(content)
        assert result == content

    def test_content_at_limit(self):
        content = "x" * CHARACTER_LIMIT
        result = check_character_limit(content)
        assert result == content

    def test_content_exceeds_limit(self):
        content = "x" * (CHARACTER_LIMIT + 1000)
        result = check_character_limit(content)
        assert len(result) > CHARACTER_LIMIT  # Includes truncation message
        assert "TRUNCATED" in result
        assert str(CHARACTER_LIMIT) in result
        assert str(CHARACTER_LIMIT + 1000) in result

    def test_empty_content(self):
        result = check_character_limit("")
        assert result == ""

    def test_custom_data_type_in_message(self):
        content = "x" * (CHARACTER_LIMIT + 100)
        result = check_character_limit(content, "test data")
        assert "TRUNCATED" in result
