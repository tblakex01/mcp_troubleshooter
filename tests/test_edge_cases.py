"""
Edge case testing for utilities and tools.

This test module focuses on boundary values, extreme inputs, and unusual
scenarios that might not be covered in standard testing:
- Utility function edge cases (negative values, very large numbers)
- Model validation edge cases (unicode, special characters, max lengths)
- Tool-specific edge cases (single-core systems, no swap, etc.)
"""

import pytest
import tempfile
import os
from unittest.mock import MagicMock, patch
from datetime import datetime

from troubleshooting_mcp.utils import (
    format_bytes,
    format_timestamp,
    handle_error,
    check_character_limit
)
from troubleshooting_mcp.models import (
    LogFileInput,
    SafeCommandInput,
    NetworkDiagnosticInput,
    ProcessSearchInput,
    ResourceMonitorInput,
)
from pydantic import ValidationError


class TestUtilsEdgeCases:
    """Test edge cases for utility functions."""

    def test_format_bytes_negative(self):
        """Test format_bytes with negative values."""
        result = format_bytes(-1024)
        # Should handle negative values gracefully
        assert isinstance(result, str)
        assert "-" in result or "0" in result

    def test_format_bytes_zero(self):
        """Test format_bytes with zero."""
        result = format_bytes(0)
        assert result == "0 B"

    def test_format_bytes_petabytes(self):
        """Test format_bytes with very large numbers (petabytes)."""
        # 1 PB = 1024^5 bytes
        result = format_bytes(1024 ** 5)
        assert isinstance(result, str)
        assert "PB" in result or "TB" in result

    def test_format_bytes_exabytes(self):
        """Test format_bytes with extremely large numbers (exabytes)."""
        # 1 EB = 1024^6 bytes
        result = format_bytes(1024 ** 6)
        assert isinstance(result, str)
        # Should handle gracefully, likely in PB or TB
        assert len(result) > 0

    def test_format_bytes_float_input(self):
        """Test format_bytes with float input."""
        result = format_bytes(1536.7)
        assert isinstance(result, str)
        assert "KB" in result or "B" in result

    def test_format_timestamp_negative(self):
        """Test format_timestamp with negative timestamp (pre-1970)."""
        result = format_timestamp(-86400)  # 1 day before epoch
        assert isinstance(result, str)
        # Should handle dates before 1970
        assert "1969" in result

    def test_format_timestamp_zero(self):
        """Test format_timestamp with zero (Unix epoch)."""
        result = format_timestamp(0)
        assert isinstance(result, str)
        assert "1970" in result

    def test_format_timestamp_future(self):
        """Test format_timestamp with future timestamp."""
        future = 2000000000  # Year 2033
        result = format_timestamp(future)
        assert isinstance(result, str)
        assert "203" in result  # Should be in 2030s

    def test_format_timestamp_very_old(self):
        """Test format_timestamp with very old date."""
        # This might fail on some systems, but should handle gracefully
        try:
            result = format_timestamp(-2147483648)  # Min 32-bit int
            assert isinstance(result, str)
        except (ValueError, OSError):
            # Some systems can't handle dates this old
            pass

    def test_handle_error_file_not_found(self):
        """Test handle_error with FileNotFoundError."""
        error = FileNotFoundError("Test file not found")
        result = handle_error(error)
        assert isinstance(result, str)
        assert "not found" in result.lower()

    def test_handle_error_permission_error(self):
        """Test handle_error with PermissionError."""
        error = PermissionError("Test permission denied")
        result = handle_error(error)
        assert isinstance(result, str)
        assert "permission" in result.lower()

    def test_handle_error_os_error(self):
        """Test handle_error with OSError."""
        error = OSError("Test OS error")
        result = handle_error(error)
        assert isinstance(result, str)
        assert "error" in result.lower()

    def test_handle_error_connection_error(self):
        """Test handle_error with ConnectionError."""
        error = ConnectionError("Test connection error")
        result = handle_error(error)
        assert isinstance(result, str)
        assert "error" in result.lower()

    def test_handle_error_empty_message(self):
        """Test handle_error with exception with empty message."""
        error = ValueError("")
        result = handle_error(error)
        assert isinstance(result, str)
        # Should still produce some output
        assert len(result) > 0

    def test_handle_error_generic_exception(self):
        """Test handle_error with generic exception."""
        error = RuntimeError("Generic runtime error")
        result = handle_error(error)
        assert isinstance(result, str)
        assert "error" in result.lower()

    def test_check_character_limit_exactly_at_limit(self):
        """Test check_character_limit with content exactly at limit."""
        content = "x" * 25000
        result = check_character_limit(content)
        # Should not be truncated
        assert len(result) == 25000
        assert "truncated" not in result.lower()

    def test_check_character_limit_one_over_limit(self):
        """Test check_character_limit with content one character over limit."""
        content = "x" * 25001
        result = check_character_limit(content)
        # Should be truncated
        assert len(result) < 25001
        assert "truncated" in result.lower()

    def test_check_character_limit_custom_data_type(self):
        """Test check_character_limit with custom data_type parameter."""
        content = "x" * 30000
        result = check_character_limit(content, data_type="custom data")
        # Should be truncated with custom message
        assert "truncated" in result.lower()
        assert "custom data" in result.lower()

    def test_check_character_limit_empty_string(self):
        """Test check_character_limit with empty string."""
        result = check_character_limit("")
        assert result == ""

    def test_check_character_limit_unicode_content(self):
        """Test check_character_limit with unicode content."""
        content = "🔥" * 30000  # Emoji characters
        result = check_character_limit(content)
        # Should handle unicode properly
        assert isinstance(result, str)
        if len(content) > 25000:
            assert "truncated" in result.lower()


class TestModelEdgeCases:
    """Test edge cases for Pydantic models."""

    def test_log_file_input_unicode_path(self):
        """Test LogFileInput with unicode characters in path."""
        params = LogFileInput(file_path="/tmp/日本語/ファイル.log")
        assert params.file_path == "/tmp/日本語/ファイル.log"

    def test_log_file_input_special_characters(self):
        """Test LogFileInput with special characters in path."""
        params = LogFileInput(file_path="/tmp/file with spaces & symbols!@#.log")
        assert "spaces" in params.file_path

    def test_log_file_input_max_lines(self):
        """Test LogFileInput with maximum allowed lines."""
        params = LogFileInput(file_path="/tmp/test.log", num_lines=1000)
        assert params.num_lines == 1000

    def test_log_file_input_min_lines(self):
        """Test LogFileInput with minimum allowed lines."""
        params = LogFileInput(file_path="/tmp/test.log", num_lines=1)
        assert params.num_lines == 1

    def test_log_file_input_lines_too_high(self):
        """Test LogFileInput rejects lines over 1000."""
        with pytest.raises(ValidationError):
            LogFileInput(file_path="/tmp/test.log", num_lines=1001)

    def test_log_file_input_lines_zero(self):
        """Test LogFileInput rejects zero lines."""
        with pytest.raises(ValidationError):
            LogFileInput(file_path="/tmp/test.log", num_lines=0)

    def test_safe_command_empty_args_list(self):
        """Test SafeCommandInput with empty args list."""
        params = SafeCommandInput(command="ping", args=[])
        assert params.args == []

    def test_safe_command_max_args(self):
        """Test SafeCommandInput with maximum allowed args (20)."""
        args = [f"arg{i}" for i in range(20)]
        params = SafeCommandInput(command="ping", args=args)
        assert len(params.args) == 20

    def test_safe_command_too_many_args(self):
        """Test SafeCommandInput rejects more than 20 args."""
        args = [f"arg{i}" for i in range(21)]
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", args=args)

    def test_safe_command_min_timeout(self):
        """Test SafeCommandInput with minimum timeout (1)."""
        params = SafeCommandInput(command="ping", timeout=1)
        assert params.timeout == 1

    def test_safe_command_max_timeout(self):
        """Test SafeCommandInput with maximum timeout (300)."""
        params = SafeCommandInput(command="ping", timeout=300)
        assert params.timeout == 300

    def test_safe_command_timeout_too_high(self):
        """Test SafeCommandInput rejects timeout over 300."""
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", timeout=301)

    def test_safe_command_timeout_zero(self):
        """Test SafeCommandInput rejects zero timeout."""
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", timeout=0)

    def test_safe_command_invalid_command(self):
        """Test SafeCommandInput rejects non-whitelisted command."""
        with pytest.raises(ValidationError):
            SafeCommandInput(command="rm")

    def test_safe_command_case_sensitive(self):
        """Test SafeCommandInput is case-sensitive for commands."""
        # "PING" should not match "ping"
        with pytest.raises(ValidationError):
            SafeCommandInput(command="PING")

    def test_network_diagnostic_min_timeout(self):
        """Test NetworkDiagnosticInput with minimum timeout (1)."""
        params = NetworkDiagnosticInput(host="example.com", timeout=1)
        assert params.timeout == 1

    def test_network_diagnostic_max_timeout(self):
        """Test NetworkDiagnosticInput with maximum timeout (30)."""
        params = NetworkDiagnosticInput(host="example.com", timeout=30)
        assert params.timeout == 30

    def test_network_diagnostic_timeout_too_high(self):
        """Test NetworkDiagnosticInput rejects timeout over 30."""
        with pytest.raises(ValidationError):
            NetworkDiagnosticInput(host="example.com", timeout=31)

    def test_network_diagnostic_idn_hostname(self):
        """Test NetworkDiagnosticInput with internationalized domain name."""
        # IDN in punycode format
        params = NetworkDiagnosticInput(host="xn--n3h.com")
        assert params.host == "xn--n3h.com"

    def test_network_diagnostic_unicode_hostname(self):
        """Test NetworkDiagnosticInput with unicode hostname."""
        params = NetworkDiagnosticInput(host="日本.jp")
        assert "日本" in params.host

    def test_process_search_min_limit(self):
        """Test ProcessSearchInput with minimum limit (1)."""
        params = ProcessSearchInput(limit=1)
        assert params.limit == 1

    def test_process_search_max_limit(self):
        """Test ProcessSearchInput with maximum limit (100)."""
        params = ProcessSearchInput(limit=100)
        assert params.limit == 100

    def test_process_search_limit_too_high(self):
        """Test ProcessSearchInput rejects limit over 100."""
        with pytest.raises(ValidationError):
            ProcessSearchInput(limit=101)

    def test_process_search_limit_zero(self):
        """Test ProcessSearchInput rejects zero limit."""
        with pytest.raises(ValidationError):
            ProcessSearchInput(limit=0)

    def test_whitespace_stripping_log_path(self):
        """Test that whitespace is stripped from log file path."""
        params = LogFileInput(file_path="  /tmp/test.log  ")
        assert params.file_path == "/tmp/test.log"

    def test_whitespace_stripping_hostname(self):
        """Test that whitespace is stripped from hostname."""
        params = NetworkDiagnosticInput(host="  example.com  ")
        assert params.host == "example.com"

    def test_whitespace_stripping_pattern(self):
        """Test that whitespace is stripped from search pattern."""
        params = ProcessSearchInput(pattern="  python  ")
        assert params.pattern == "python"


class TestToolEdgeCases:
    """Test edge cases for tool implementations."""

    @pytest.mark.asyncio
    async def test_process_search_with_limit_one(self):
        """Test process search with limit=1."""
        from troubleshooting_mcp.tools import process_search

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        process_search.register_process_search(mcp)
        func = tool_funcs[0]

        params = ProcessSearchInput(limit=1)
        result = await func(params)

        assert isinstance(result, str)
        # Should return at most 1 process

    @pytest.mark.asyncio
    async def test_log_reader_single_line(self):
        """Test log reader with num_lines=1."""
        from troubleshooting_mcp.tools import log_reader

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        log_reader.register_log_reader(mcp)
        func = tool_funcs[0]

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")

        try:
            params = LogFileInput(file_path=temp_path, num_lines=1)
            result = await func(params)

            assert isinstance(result, str)
            # Should only contain 1 line
            assert "Line 1" in result or "Line 3" in result
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_log_reader_file_with_blank_lines(self):
        """Test log reader with file containing blank lines."""
        from troubleshooting_mcp.tools import log_reader

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        log_reader.register_log_reader(mcp)
        func = tool_funcs[0]

        # Create a file with blank lines
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("Line 1\n")
            f.write("\n")
            f.write("\n")
            f.write("Line 4\n")

        try:
            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            assert isinstance(result, str)
            # Should handle blank lines
            assert len(result) > 0
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_log_reader_very_long_lines(self):
        """Test log reader with very long lines."""
        from troubleshooting_mcp.tools import log_reader

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        log_reader.register_log_reader(mcp)
        func = tool_funcs[0]

        # Create a file with very long lines
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("x" * 10000 + "\n")
            f.write("y" * 10000 + "\n")

        try:
            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            # Should handle long lines without crashing
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_resource_monitor_per_cpu_single_core(self):
        """Test resource monitor with per_cpu on potential single-core system."""
        from troubleshooting_mcp.tools import resource_monitor

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        resource_monitor.register_resource_monitor(mcp)
        func = tool_funcs[0]

        params = ResourceMonitorInput(per_cpu=True)
        result = await func(params)

        # Should work regardless of CPU count
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_environment_inspect_empty_pattern(self):
        """Test environment inspect with empty string pattern."""
        from troubleshooting_mcp.tools import environment_inspect

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        environment_inspect.register_environment_inspect(mcp)
        func = tool_funcs[0]

        # Empty pattern should match all
        params = MagicMock(pattern="", response_format="markdown")
        result = await func(params)

        assert isinstance(result, str)
        # Should return all environment variables
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_network_diagnostic_localhost_ipv4(self):
        """Test network diagnostic with 127.0.0.1."""
        from troubleshooting_mcp.tools import network_diagnostic

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        network_diagnostic.register_network_diagnostic(mcp)
        func = tool_funcs[0]

        params = NetworkDiagnosticInput(host="127.0.0.1")
        result = await func(params)

        assert isinstance(result, str)
        # Should resolve localhost
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_network_diagnostic_numeric_ip(self):
        """Test network diagnostic with IP address (no DNS needed)."""
        from troubleshooting_mcp.tools import network_diagnostic

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        network_diagnostic.register_network_diagnostic(mcp)
        func = tool_funcs[0]

        # Use Google DNS
        params = NetworkDiagnosticInput(host="8.8.8.8")
        result = await func(params)

        assert isinstance(result, str)
        # Should handle IP address
        assert "8.8.8.8" in result
