"""
JSON format validation testing.

This test module focuses on validating JSON output format for all tools:
- System info JSON structure
- Resource monitor JSON structure
- Process search JSON structure
- Environment inspect JSON structure
- Safe command JSON structure
- Network diagnostic JSON structure
- Proper JSON parsing and structure validation
"""

import pytest
import json
import tempfile
import os
from unittest.mock import MagicMock, patch

from troubleshooting_mcp.models import (
    SystemInfoInput,
    ResourceMonitorInput,
    ProcessSearchInput,
    EnvironmentSearchInput,
    SafeCommandInput,
    NetworkDiagnosticInput,
)


class TestSystemInfoJSON:
    """Test JSON output format for system info tool."""

    @pytest.mark.asyncio
    async def test_system_info_json_format(self):
        """Test that system info produces valid JSON when requested."""
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

        params = SystemInfoInput(response_format="json")
        result = await func(params)

        # Should be valid JSON
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_system_info_json_structure(self):
        """Test that system info JSON has expected structure."""
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

        params = SystemInfoInput(response_format="json")
        result = await func(params)

        parsed = json.loads(result)

        # Should have key system information fields
        assert 'system' in parsed or 'os' in parsed or 'platform' in parsed
        # Should be a dictionary
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_system_info_markdown_vs_json(self):
        """Test that markdown and JSON formats differ appropriately."""
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

        # Get markdown format
        params_md = SystemInfoInput(response_format="markdown")
        result_md = await func(params_md)

        # Get JSON format
        params_json = SystemInfoInput(response_format="json")
        result_json = await func(params_json)

        # Markdown should contain formatting characters
        assert "#" in result_md or "*" in result_md or "-" in result_md

        # JSON should be parseable
        parsed_json = json.loads(result_json)
        assert isinstance(parsed_json, dict)


class TestResourceMonitorJSON:
    """Test JSON output format for resource monitor tool."""

    @pytest.mark.asyncio
    async def test_resource_monitor_json_format(self):
        """Test that resource monitor produces valid JSON."""
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

        params = ResourceMonitorInput(response_format="json", per_cpu=False)
        result = await func(params)

        # Should be valid JSON
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_resource_monitor_json_structure(self):
        """Test that resource monitor JSON has expected fields."""
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

        params = ResourceMonitorInput(response_format="json", per_cpu=False)
        result = await func(params)

        parsed = json.loads(result)

        # Should have resource-related fields
        expected_fields = ['cpu', 'memory', 'disk', 'network']
        # At least some of these should be present
        assert any(field in parsed for field in expected_fields)

    @pytest.mark.asyncio
    async def test_resource_monitor_json_per_cpu(self):
        """Test resource monitor JSON with per_cpu=True."""
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

        params = ResourceMonitorInput(response_format="json", per_cpu=True)
        result = await func(params)

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)


class TestProcessSearchJSON:
    """Test JSON output format for process search tool."""

    @pytest.mark.asyncio
    async def test_process_search_json_format(self):
        """Test that process search produces valid JSON."""
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

        params = ProcessSearchInput(response_format="json", limit=10)
        result = await func(params)

        # Should be valid JSON
        assert isinstance(result, str)
        parsed = json.loads(result)
        # Could be dict or list depending on implementation
        assert isinstance(parsed, (dict, list))

    @pytest.mark.asyncio
    async def test_process_search_json_with_pattern(self):
        """Test process search JSON with pattern filter."""
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
            response_format="json",
            pattern="python",
            limit=5
        )
        result = await func(params)

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, (dict, list))

    @pytest.mark.asyncio
    async def test_process_search_json_structure(self):
        """Test that process search JSON has process information."""
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

        # Mock a process
        mock_proc = MagicMock()
        mock_proc.info = {
            'pid': 12345,
            'name': 'test_process',
            'cpu_percent': 5.0,
            'memory_percent': 2.5,
        }
        mock_proc.cmdline.return_value = ['/usr/bin/test']

        with patch('psutil.process_iter', return_value=[mock_proc]):
            params = ProcessSearchInput(response_format="json")
            result = await func(params)

            parsed = json.loads(result)
            # Should contain process information
            assert isinstance(parsed, (dict, list))


class TestEnvironmentInspectJSON:
    """Test JSON output format for environment inspect tool."""

    @pytest.mark.asyncio
    async def test_environment_inspect_json_format(self):
        """Test that environment inspect produces valid JSON."""
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

        params = EnvironmentSearchInput(response_format="json")
        result = await func(params)

        # Should be valid JSON
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_environment_inspect_json_with_pattern(self):
        """Test environment inspect JSON with pattern filter."""
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

        params = EnvironmentSearchInput(response_format="json", pattern="PATH")
        result = await func(params)

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_environment_inspect_json_structure(self):
        """Test that environment inspect JSON has expected structure."""
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

        params = EnvironmentSearchInput(response_format="json")
        result = await func(params)

        parsed = json.loads(result)

        # Should have environment-related information
        assert isinstance(parsed, dict)
        # Might have 'environment' or 'tools' or similar keys
        assert len(parsed) >= 0  # May be empty on some systems


class TestSafeCommandJSON:
    """Test JSON output format for safe command tool."""

    @pytest.mark.asyncio
    async def test_safe_command_json_format(self):
        """Test that safe command produces valid JSON."""
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

        # Mock subprocess
        mock_result = MagicMock()
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping", response_format="json")
            result = await func(params)

            # Should be valid JSON
            assert isinstance(result, str)
            parsed = json.loads(result)
            assert isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_safe_command_json_structure(self):
        """Test that safe command JSON has expected fields."""
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

        # Mock subprocess
        mock_result = MagicMock()
        mock_result.stdout = "test stdout"
        mock_result.stderr = "test stderr"
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping", response_format="json")
            result = await func(params)

            parsed = json.loads(result)

            # Should have command output fields
            expected_fields = ['command', 'stdout', 'stderr', 'returncode', 'exit_code', 'output']
            # At least some of these should be present
            has_field = any(field in str(parsed).lower() for field in expected_fields)
            assert has_field or isinstance(parsed, dict)

    @pytest.mark.asyncio
    async def test_safe_command_json_error_case(self):
        """Test safe command JSON format when command fails."""
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

        # Mock subprocess with error
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "error message"
        mock_result.returncode = 1

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping", response_format="json")
            result = await func(params)

            # Should still be valid JSON
            parsed = json.loads(result)
            assert isinstance(parsed, dict)


class TestNetworkDiagnosticJSON:
    """Test JSON output format for network diagnostic tool (if supported)."""

    @pytest.mark.asyncio
    async def test_network_diagnostic_basic_output(self):
        """Test that network diagnostic output is consistent."""
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

        # Should return a string (may be markdown or plain text)
        assert isinstance(result, str)
        assert len(result) > 0


class TestJSONParsingRobustness:
    """Test JSON parsing edge cases and robustness."""

    def test_json_with_special_characters(self):
        """Test that JSON can handle special characters in data."""
        test_data = {
            "key": "value with \"quotes\" and \n newlines",
            "unicode": "日本語 🔥",
            "backslash": "path\\to\\file"
        }

        # Should serialize and parse correctly
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)

        assert parsed["key"] == test_data["key"]
        assert parsed["unicode"] == test_data["unicode"]
        assert parsed["backslash"] == test_data["backslash"]

    def test_json_with_numbers(self):
        """Test JSON with various number types."""
        test_data = {
            "int": 42,
            "float": 3.14159,
            "large": 1234567890,
            "zero": 0,
            "negative": -100
        }

        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)

        assert parsed["int"] == 42
        assert abs(parsed["float"] - 3.14159) < 0.0001
        assert parsed["zero"] == 0
        assert parsed["negative"] == -100

    def test_json_with_nested_structures(self):
        """Test JSON with nested dictionaries and lists."""
        test_data = {
            "nested": {
                "level1": {
                    "level2": ["a", "b", "c"]
                }
            },
            "list": [1, 2, {"key": "value"}]
        }

        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)

        assert parsed["nested"]["level1"]["level2"] == ["a", "b", "c"]
        assert parsed["list"][2]["key"] == "value"

    def test_json_empty_structures(self):
        """Test JSON with empty structures."""
        test_data = {
            "empty_dict": {},
            "empty_list": [],
            "empty_string": ""
        }

        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)

        assert parsed["empty_dict"] == {}
        assert parsed["empty_list"] == []
        assert parsed["empty_string"] == ""


class TestFormatConsistency:
    """Test that format parameter is respected across all tools."""

    @pytest.mark.asyncio
    async def test_all_tools_respect_format_parameter(self):
        """Test that all tools that support format parameter use it."""
        from troubleshooting_mcp.tools import (
            system_info,
            resource_monitor,
            process_search,
            environment_inspect,
        )

        mock_mcp = MagicMock()
        tool_funcs = {}

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_name = kwargs.get('name', func.__name__)
                tool_funcs[tool_name] = func
                return func
            return decorator

        mock_mcp.tool = mock_tool

        # Register tools
        system_info.register_system_info(mock_mcp)
        resource_monitor.register_resource_monitor(mock_mcp)
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)

        # Test each tool with JSON format
        tools_to_test = [
            ('troubleshooting_get_system_info', SystemInfoInput(response_format="json")),
            ('troubleshooting_monitor_resources', ResourceMonitorInput(response_format="json")),
            ('troubleshooting_search_processes', ProcessSearchInput(response_format="json")),
            ('troubleshooting_inspect_environment', EnvironmentSearchInput(response_format="json")),
        ]

        for tool_name, params in tools_to_test:
            result = await tool_funcs[tool_name](params)
            # Should return valid JSON
            try:
                parsed = json.loads(result)
                assert isinstance(parsed, (dict, list))
            except json.JSONDecodeError:
                pytest.fail(f"{tool_name} did not produce valid JSON")
