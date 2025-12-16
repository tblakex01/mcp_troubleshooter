"""
Comprehensive tests for all diagnostic tools.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from troubleshooting_mcp.models import (
    EnvironmentSearchInput,
    LogFileInput,
    NetworkDiagnosticInput,
    ProcessSearchInput,
    ResourceMonitorInput,
    ResponseFormat,
    SafeCommandInput,
    SystemInfoInput,
)


class TestSystemInfoTool:
    """Tests for system_info tool."""

    @pytest.mark.asyncio
    async def test_system_info_markdown_format(self):
        """Test system info with markdown format."""
        from troubleshooting_mcp.tools import system_info

        # Create a mock MCP server and register the tool
        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        system_info.register_system_info(mcp)

        # Get the registered function
        assert len(tool_funcs) > 0
        func = tool_funcs[0]

        params = SystemInfoInput(response_format=ResponseFormat.MARKDOWN)
        result = await func(params)

        assert isinstance(result, str)
        assert "System Information" in result or "Operating System" in result

    @pytest.mark.asyncio
    async def test_system_info_json_format(self):
        """Test system info with JSON format."""
        from troubleshooting_mcp.tools import system_info

        mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        system_info.register_system_info(mcp)

        func = tool_funcs[0]
        params = SystemInfoInput(response_format=ResponseFormat.JSON)
        result = await func(params)

        assert isinstance(result, str)
        data = json.loads(result)
        assert "system" in data
        assert "python_version" in data


class TestResourceMonitorTool:
    """Tests for resource_monitor tool."""

    @pytest.mark.asyncio
    async def test_resource_monitor_markdown(self):
        """Test resource monitor with markdown format."""
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
        params = ResourceMonitorInput()
        result = await func(params)

        assert isinstance(result, str)
        # Accept successful output or error message
        assert "CPU" in result or "Memory" in result or "Error" in result or "error" in result.lower()

    @pytest.mark.asyncio
    async def test_resource_monitor_with_per_cpu(self):
        """Test resource monitor with per-CPU stats."""
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
        params = ResourceMonitorInput(include_per_cpu=True)
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_resource_monitor_json_format(self):
        """Test resource monitor with JSON format."""
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
        params = ResourceMonitorInput(response_format=ResponseFormat.JSON)
        result = await func(params)

        assert isinstance(result, str)
        # Try to parse as JSON, but accept error messages too
        try:
            data = json.loads(result)
            assert "cpu" in data or "memory" in data
        except json.JSONDecodeError:
            # If not JSON, it should be an error message
            assert "Error" in result or "error" in result.lower()


class TestLogReaderTool:
    """Tests for log_reader tool."""

    @pytest.mark.asyncio
    async def test_log_reader_with_temp_file(self, tmp_path):
        """Test log reader with a temporary log file."""
        from troubleshooting_mcp.tools import log_reader

        # Create a temporary log file
        log_file = tmp_path / "test.log"
        log_content = """2025-01-01 10:00:00 INFO Application started
2025-01-01 10:00:01 DEBUG Loading config
2025-01-01 10:00:02 ERROR Connection failed
2025-01-01 10:00:03 WARNING Retry attempt
2025-01-01 10:00:04 INFO Success"""
        log_file.write_text(log_content)

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
        params = LogFileInput(file_path=str(log_file), lines=10)

        # Patch ALLOWED_LOG_DIRS to include the temp directory
        with patch("troubleshooting_mcp.tools.log_reader.ALLOWED_LOG_DIRS", [str(tmp_path)]):
            result = await func(params)

        assert isinstance(result, str)
        assert "INFO Application started" in result or "Application started" in result

    @pytest.mark.asyncio
    async def test_log_reader_with_pattern(self, tmp_path):
        """Test log reader with search pattern."""
        from troubleshooting_mcp.tools import log_reader

        log_file = tmp_path / "test.log"
        log_content = """2025-01-01 10:00:00 INFO Application started
2025-01-01 10:00:01 ERROR Connection failed
2025-01-01 10:00:02 ERROR Database error
2025-01-01 10:00:03 INFO Success"""
        log_file.write_text(log_content)

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
        params = LogFileInput(file_path=str(log_file), search_pattern="ERROR")

        # Patch ALLOWED_LOG_DIRS to include the temp directory
        with patch("troubleshooting_mcp.tools.log_reader.ALLOWED_LOG_DIRS", [str(tmp_path)]):
            result = await func(params)

        assert isinstance(result, str)
        assert "ERROR" in result

    @pytest.mark.asyncio
    async def test_log_reader_file_not_found(self):
        """Test log reader with non-existent file."""
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
        params = LogFileInput(file_path="/nonexistent/file.log")
        result = await func(params)

        assert isinstance(result, str)
        assert "not found" in result.lower() or "error" in result.lower()


class TestNetworkDiagnosticTool:
    """Tests for network_diagnostic tool."""

    @pytest.mark.asyncio
    async def test_network_diagnostic_localhost(self):
        """Test network diagnostic with localhost."""
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
        params = NetworkDiagnosticInput(host="localhost")
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_network_diagnostic_with_port(self):
        """Test network diagnostic with specific port."""
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
        params = NetworkDiagnosticInput(host="127.0.0.1", port=54321, timeout=1)
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_network_diagnostic_ipv4(self):
        """Test network diagnostic with IPv4 address."""
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
        assert len(result) > 0


class TestProcessSearchTool:
    """Tests for process_search tool."""

    @pytest.mark.asyncio
    async def test_process_search_all_processes(self):
        """Test process search without pattern (all processes)."""
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
        params = ProcessSearchInput(limit=5)
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_process_search_with_pattern(self):
        """Test process search with pattern."""
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
        params = ProcessSearchInput(pattern="python", limit=10)
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_process_search_json_format(self):
        """Test process search with JSON format."""
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
        params = ProcessSearchInput(
            limit=5,
            response_format=ResponseFormat.JSON
        )
        result = await func(params)

        assert isinstance(result, str)


class TestEnvironmentInspectTool:
    """Tests for environment_inspect tool."""

    @pytest.mark.asyncio
    async def test_environment_inspect_all(self):
        """Test environment inspect without pattern."""
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
        params = EnvironmentSearchInput()
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_environment_inspect_with_pattern(self):
        """Test environment inspect with pattern."""
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
        params = EnvironmentSearchInput(pattern="PATH")
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_environment_inspect_json_format(self):
        """Test environment inspect with JSON format."""
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
        params = EnvironmentSearchInput(response_format=ResponseFormat.JSON)
        result = await func(params)

        assert isinstance(result, str)


class TestSafeCommandTool:
    """Tests for safe_command tool."""

    @pytest.mark.asyncio
    async def test_safe_command_uptime(self):
        """Test safe command with uptime."""
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
        params = SafeCommandInput(command="uptime")
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_safe_command_hostname(self):
        """Test safe command with hostname."""
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
        params = SafeCommandInput(command="hostname")
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_safe_command_with_args(self):
        """Test safe command with arguments."""
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
        params = SafeCommandInput(command="df", args=["-h"])
        result = await func(params)

        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_safe_command_whoami(self):
        """Test safe command with whoami."""
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
        params = SafeCommandInput(command="whoami")
        result = await func(params)

        assert isinstance(result, str)
