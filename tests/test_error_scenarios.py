"""
Comprehensive error scenario testing for all tools.

This test module focuses on error handling paths that are often missed in basic
happy-path testing. It covers:
- Network failures (timeout, connection refused, DNS errors)
- File system errors (permission denied, file not found, binary files)
- Command execution errors (timeout, not found, non-zero exit)
- Process access errors (access denied, zombie processes)
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
import socket
import subprocess

from troubleshooting_mcp.models import (
    NetworkDiagnosticInput,
    LogFileInput,
    SafeCommandInput,
    ProcessSearchInput,
)


class TestNetworkDiagnosticErrors:
    """Test error scenarios in network diagnostic tool."""

    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """Test handling of connection timeout with unreachable host."""
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

        # Use TEST-NET-1 address (192.0.2.0/24) which should be unreachable
        params = NetworkDiagnosticInput(
            host="192.0.2.1",
            port=12345,
            timeout=1
        )
        result = await func(params)

        assert isinstance(result, str)
        # Should indicate timeout or unreachable
        assert any(keyword in result.lower() for keyword in ['timeout', 'timed out', 'failed', 'closed'])

    @pytest.mark.asyncio
    async def test_connection_refused(self):
        """Test handling of connection refused on closed port."""
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

        # Test with localhost on a port that's likely closed
        params = NetworkDiagnosticInput(
            host="127.0.0.1",
            port=54321,
            timeout=2
        )
        result = await func(params)

        assert isinstance(result, str)
        # Should indicate connection refused or closed
        assert any(keyword in result for keyword in ['Refused', 'CLOSED', 'Failed', 'refused'])

    @pytest.mark.asyncio
    async def test_dns_resolution_failure(self):
        """Test handling of DNS resolution failure with invalid hostname."""
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

        # Use .invalid TLD which should never resolve
        params = NetworkDiagnosticInput(
            host="this-domain-definitely-does-not-exist-12345.invalid"
        )
        result = await func(params)

        assert isinstance(result, str)
        # Should indicate DNS failure
        assert any(keyword in result for keyword in ['Failed', 'Cannot resolve', 'failed', 'error'])

    @pytest.mark.asyncio
    async def test_ipv6_localhost(self):
        """Test IPv6 address handling."""
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

        # Test with IPv6 localhost
        params = NetworkDiagnosticInput(host="::1")
        result = await func(params)

        assert isinstance(result, str)
        # Should either resolve successfully or fail gracefully
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_socket_generic_error(self):
        """Test handling of generic socket errors."""
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

        # Mock socket.create_connection to raise a generic socket error
        with patch('socket.create_connection', side_effect=socket.error("Mock socket error")):
            params = NetworkDiagnosticInput(host="example.com", port=80)
            result = await func(params)

            assert isinstance(result, str)
            assert "error" in result.lower() or "failed" in result.lower()


class TestLogReaderErrors:
    """Test error scenarios in log reader tool."""

    @pytest.mark.asyncio
    async def test_file_not_found(self):
        """Test handling of non-existent file."""
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

        params = LogFileInput(file_path="/nonexistent/path/to/file.log")
        result = await func(params)

        assert isinstance(result, str)
        assert "not found" in result.lower() or "does not exist" in result.lower()

    @pytest.mark.asyncio
    async def test_directory_path(self):
        """Test handling of directory path instead of file."""
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

        # Use /tmp directory which should exist
        params = LogFileInput(file_path="/tmp")
        result = await func(params)

        assert isinstance(result, str)
        assert "not a file" in result.lower() or "directory" in result.lower()

    @pytest.mark.asyncio
    async def test_permission_denied(self):
        """Test handling of permission denied error."""
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

        # Create a temporary file with no read permissions
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("test content\n")

        try:
            # Remove read permissions
            os.chmod(temp_path, 0o000)

            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            assert isinstance(result, str)
            assert "permission" in result.lower() or "denied" in result.lower()
        finally:
            # Restore permissions and clean up
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_empty_file(self):
        """Test handling of empty log file."""
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

        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name

        try:
            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            assert isinstance(result, str)
            assert "empty" in result.lower() or "no lines" in result.lower()
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_no_pattern_matches(self):
        """Test handling when pattern doesn't match any lines."""
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

        # Create a temporary file with content that won't match pattern
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("line 1\n")
            f.write("line 2\n")
            f.write("line 3\n")

        try:
            params = LogFileInput(
                file_path=temp_path,
                search_pattern="THISWILLNEVERMATCH12345"
            )
            result = await func(params)

            assert isinstance(result, str)
            assert "no lines found" in result.lower() or "no matching" in result.lower()
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_binary_file(self):
        """Test handling of binary file (errors='ignore' should handle it)."""
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

        # Create a binary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            temp_path = f.name
            f.write(b'\x00\x01\x02\x03\x04\x05\xff\xfe\xfd')

        try:
            params = LogFileInput(file_path=temp_path, num_lines=10)
            result = await func(params)

            # Should not crash, may return empty or partial content
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)


class TestSafeCommandErrors:
    """Test error scenarios in safe command executor."""

    @pytest.mark.asyncio
    async def test_command_not_found(self):
        """Test handling of command not found on system."""
        from troubleshooting_mcp.tools import safe_command

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        safe_command.register_safe_command(mcp)
        func = tool_funcs[0]

        # Mock subprocess to raise FileNotFoundError
        with patch('subprocess.run', side_effect=FileNotFoundError("Command not found")):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            assert isinstance(result, str)
            assert "not found" in result.lower() or "error" in result.lower()

    @pytest.mark.asyncio
    async def test_command_timeout(self):
        """Test handling of command timeout."""
        from troubleshooting_mcp.tools import safe_command

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        safe_command.register_safe_command(mcp)
        func = tool_funcs[0]

        # Mock subprocess to raise TimeoutExpired
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("ping", 1)):
            params = SafeCommandInput(command="ping", timeout=1)
            result = await func(params)

            assert isinstance(result, str)
            assert "timeout" in result.lower() or "timed out" in result.lower()

    @pytest.mark.asyncio
    async def test_command_with_stderr_only(self):
        """Test handling of command with only stderr output."""
        from troubleshooting_mcp.tools import safe_command

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        safe_command.register_safe_command(mcp)
        func = tool_funcs[0]

        # Mock subprocess to return only stderr
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Error message here"
        mock_result.returncode = 1

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            assert isinstance(result, str)
            assert "Error message here" in result

    @pytest.mark.asyncio
    async def test_command_non_zero_exit(self):
        """Test handling of command with non-zero exit code."""
        from troubleshooting_mcp.tools import safe_command

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        safe_command.register_safe_command(mcp)
        func = tool_funcs[0]

        # Mock subprocess to return non-zero exit code
        mock_result = MagicMock()
        mock_result.stdout = "Some output"
        mock_result.stderr = "Some error"
        mock_result.returncode = 127

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            assert isinstance(result, str)
            # Should include exit code information
            assert "127" in result or "exit" in result.lower()


class TestProcessSearchErrors:
    """Test error scenarios in process search tool."""

    @pytest.mark.asyncio
    async def test_access_denied_handling(self):
        """Test handling of AccessDenied exception."""
        from troubleshooting_mcp.tools import process_search
        import psutil

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

        # Mock process that raises AccessDenied
        mock_process = MagicMock()
        mock_process.pid = 12345
        mock_process.name.return_value = "system_process"
        mock_process.info = {
            'pid': 12345,
            'name': 'system_process',
            'cpu_percent': None,
            'memory_percent': None,
        }
        mock_process.cmdline.side_effect = psutil.AccessDenied()

        with patch('psutil.process_iter', return_value=[mock_process]):
            params = ProcessSearchInput(pattern="system")
            result = await func(params)

            # Should handle gracefully without crashing
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_no_cmdline_process(self):
        """Test handling of process with no command line."""
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

        # Mock process with empty cmdline
        mock_process = MagicMock()
        mock_process.info = {
            'pid': 12345,
            'name': 'kernel_process',
            'cpu_percent': 0.0,
            'memory_percent': 0.1,
        }
        mock_process.cmdline.return_value = []

        with patch('psutil.process_iter', return_value=[mock_process]):
            params = ProcessSearchInput()
            result = await func(params)

            # Should handle processes without cmdline
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_empty_process_results(self):
        """Test handling when no processes match the pattern."""
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

        params = ProcessSearchInput(pattern="THISWILLNEVERMATCHANYPROCESS12345")
        result = await func(params)

        assert isinstance(result, str)
        assert "no processes found" in result.lower() or "0 processes" in result.lower()


class TestResourceMonitorErrors:
    """Test error scenarios in resource monitor tool."""

    @pytest.mark.asyncio
    async def test_missing_disk_io_counters(self):
        """Test handling when disk I/O counters are unavailable."""
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

        # Mock disk_io_counters to return None
        with patch('psutil.disk_io_counters', return_value=None):
            params = MagicMock(response_format="markdown", per_cpu=False)
            result = await func(params)

            # Should handle gracefully
            assert isinstance(result, str)
            assert "not available" in result.lower() or "unavailable" in result.lower()

    @pytest.mark.asyncio
    async def test_missing_network_io_counters(self):
        """Test handling when network I/O counters are unavailable."""
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

        # Mock net_io_counters to return None
        with patch('psutil.net_io_counters', return_value=None):
            params = MagicMock(response_format="markdown", per_cpu=False)
            result = await func(params)

            # Should handle gracefully
            assert isinstance(result, str)
            assert "not available" in result.lower() or "unavailable" in result.lower()


class TestEnvironmentInspectErrors:
    """Test error scenarios in environment inspect tool."""

    @pytest.mark.asyncio
    async def test_pattern_no_matches(self):
        """Test handling when environment pattern matches nothing."""
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

        params = MagicMock(
            pattern="THISVARIABLEWILLNEVEREXIST12345",
            response_format="markdown"
        )
        result = await func(params)

        assert isinstance(result, str)
        # Should indicate no matches found
        assert "no environment variables" in result.lower() or "0 variables" in result.lower()

    @pytest.mark.asyncio
    async def test_tool_version_detection_failure(self):
        """Test handling when tool version detection fails."""
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

        # This should handle tools that aren't installed gracefully
        params = MagicMock(pattern=None, response_format="markdown")
        result = await func(params)

        # Should not crash even if some tools aren't available
        assert isinstance(result, str)
        assert len(result) > 0
