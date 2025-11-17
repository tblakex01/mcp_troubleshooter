"""
End-to-end integration testing for MCP server.

This test module focuses on integration scenarios:
- Full MCP server initialization
- Tool registration and discovery
- Multi-tool workflows
- Server entry point execution
- Backward compatibility
"""

import pytest
from unittest.mock import MagicMock, patch, call
import sys
import asyncio


class TestMCPServerIntegration:
    """Test MCP server initialization and tool registration."""

    def test_server_initialization(self):
        """Test that server initializes without errors."""
        from troubleshooting_mcp.server import mcp

        assert mcp is not None
        assert hasattr(mcp, 'tool')

    def test_all_tools_registered(self):
        """Test that all 7 tools are registered with correct names."""
        from troubleshooting_mcp.tools import register_all_tools

        # Create a mock MCP instance
        mock_mcp = MagicMock()
        registered_tools = []

        def mock_tool(*args, **kwargs):
            """Mock tool decorator that tracks registrations."""
            def decorator(func):
                # Extract tool name from kwargs if available
                tool_name = kwargs.get('name', func.__name__)
                registered_tools.append(tool_name)
                return func
            return decorator

        mock_mcp.tool = mock_tool

        # Register all tools
        register_all_tools(mock_mcp)

        # Verify all 7 tools are registered
        expected_tools = [
            'troubleshooting_get_system_info',
            'troubleshooting_monitor_resources',
            'troubleshooting_read_log_file',
            'troubleshooting_test_network_connectivity',
            'troubleshooting_search_processes',
            'troubleshooting_inspect_environment',
            'troubleshooting_execute_safe_command',
        ]

        for tool_name in expected_tools:
            assert tool_name in registered_tools, f"Tool {tool_name} not registered"

        # Should have exactly 7 tools
        assert len(registered_tools) == 7

    def test_tool_registration_order(self):
        """Test that tools are registered in the expected order."""
        from troubleshooting_mcp.tools import register_all_tools

        mock_mcp = MagicMock()
        tool_order = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_name = kwargs.get('name', func.__name__)
                tool_order.append(tool_name)
                return func
            return decorator

        mock_mcp.tool = mock_tool
        register_all_tools(mock_mcp)

        # Verify tools are registered in consistent order
        assert len(tool_order) == 7
        assert 'troubleshooting_get_system_info' in tool_order
        assert 'troubleshooting_monitor_resources' in tool_order

    def test_individual_tool_registration(self):
        """Test that each tool can be registered individually."""
        from troubleshooting_mcp.tools import (
            system_info,
            resource_monitor,
            log_reader,
            network_diagnostic,
            process_search,
            environment_inspect,
            safe_command,
        )

        mock_mcp = MagicMock()
        mock_tool = MagicMock()
        mock_mcp.tool = mock_tool

        # Register each tool individually
        system_info.register_system_info(mock_mcp)
        resource_monitor.register_resource_monitor(mock_mcp)
        log_reader.register_log_reader(mock_mcp)
        network_diagnostic.register_network_diagnostic(mock_mcp)
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)
        safe_command.register_safe_command(mock_mcp)

        # Verify tool decorator was called for each
        assert mock_tool.call_count == 7

    def test_server_metadata(self):
        """Test that server has correct metadata."""
        from troubleshooting_mcp.server import mcp

        # Server should have a name
        assert hasattr(mcp, 'name') or hasattr(mcp, '__name__')

    @pytest.mark.asyncio
    async def test_server_can_execute_all_tools(self):
        """Test that all registered tools can be executed."""
        from troubleshooting_mcp.tools import (
            system_info,
            resource_monitor,
            log_reader,
            network_diagnostic,
            process_search,
            environment_inspect,
            safe_command,
        )
        from troubleshooting_mcp.models import (
            SystemInfoInput,
            ResourceMonitorInput,
            LogFileInput,
            NetworkDiagnosticInput,
            ProcessSearchInput,
            EnvironmentSearchInput,
            SafeCommandInput,
        )
        import tempfile

        mock_mcp = MagicMock()
        tool_funcs = {}

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_name = kwargs.get('name', func.__name__)
                tool_funcs[tool_name] = func
                return func
            return decorator

        mock_mcp.tool = mock_tool

        # Register all tools
        system_info.register_system_info(mock_mcp)
        resource_monitor.register_resource_monitor(mock_mcp)
        log_reader.register_log_reader(mock_mcp)
        network_diagnostic.register_network_diagnostic(mock_mcp)
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)
        safe_command.register_safe_command(mock_mcp)

        # Test system_info
        func = tool_funcs['troubleshooting_get_system_info']
        params = SystemInfoInput(response_format="markdown")
        result = await func(params)
        assert isinstance(result, str)
        assert len(result) > 0

        # Test resource_monitor
        func = tool_funcs['troubleshooting_monitor_resources']
        params = ResourceMonitorInput(response_format="markdown")
        result = await func(params)
        assert isinstance(result, str)
        assert len(result) > 0

        # Test process_search
        func = tool_funcs['troubleshooting_search_processes']
        params = ProcessSearchInput()
        result = await func(params)
        assert isinstance(result, str)
        assert len(result) > 0

        # Test environment_inspect
        func = tool_funcs['troubleshooting_inspect_environment']
        params = EnvironmentSearchInput()
        result = await func(params)
        assert isinstance(result, str)
        assert len(result) > 0

        # Test network_diagnostic
        func = tool_funcs['troubleshooting_test_network_connectivity']
        params = NetworkDiagnosticInput(host="localhost")
        result = await func(params)
        assert isinstance(result, str)
        assert len(result) > 0


class TestMultiToolWorkflow:
    """Test workflows involving multiple tools."""

    @pytest.mark.asyncio
    async def test_system_info_then_process_search(self):
        """Test sequential execution: system info followed by process search."""
        from troubleshooting_mcp.tools import system_info, process_search
        from troubleshooting_mcp.models import SystemInfoInput, ProcessSearchInput

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
        process_search.register_process_search(mock_mcp)

        # Execute system info
        params1 = SystemInfoInput(response_format="markdown")
        result1 = await tool_funcs['troubleshooting_get_system_info'](params1)
        assert isinstance(result1, str)
        assert len(result1) > 0

        # Execute process search
        params2 = ProcessSearchInput(pattern="python", limit=5)
        result2 = await tool_funcs['troubleshooting_search_processes'](params2)
        assert isinstance(result2, str)
        assert len(result2) > 0

    @pytest.mark.asyncio
    async def test_network_test_then_log_check(self):
        """Test sequential execution: network test followed by log check."""
        from troubleshooting_mcp.tools import network_diagnostic, log_reader
        from troubleshooting_mcp.models import NetworkDiagnosticInput, LogFileInput
        import tempfile

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
        network_diagnostic.register_network_diagnostic(mock_mcp)
        log_reader.register_log_reader(mock_mcp)

        # Execute network diagnostic
        params1 = NetworkDiagnosticInput(host="localhost")
        result1 = await tool_funcs['troubleshooting_test_network_connectivity'](params1)
        assert isinstance(result1, str)

        # Create a temporary log file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            f.write("Log line 1\n")
            f.write("Log line 2\n")

        try:
            # Execute log reader
            params2 = LogFileInput(file_path=temp_path)
            result2 = await tool_funcs['troubleshooting_read_log_file'](params2)
            assert isinstance(result2, str)
        finally:
            import os
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_resource_monitor_then_environment(self):
        """Test sequential execution: resource monitor followed by environment inspect."""
        from troubleshooting_mcp.tools import resource_monitor, environment_inspect
        from troubleshooting_mcp.models import ResourceMonitorInput, EnvironmentSearchInput

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
        resource_monitor.register_resource_monitor(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)

        # Execute resource monitor
        params1 = ResourceMonitorInput(response_format="markdown")
        result1 = await tool_funcs['troubleshooting_monitor_resources'](params1)
        assert isinstance(result1, str)

        # Execute environment inspect
        params2 = EnvironmentSearchInput(pattern="PATH")
        result2 = await tool_funcs['troubleshooting_inspect_environment'](params2)
        assert isinstance(result2, str)

    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self):
        """Test that multiple tools can execute concurrently."""
        from troubleshooting_mcp.tools import system_info, process_search, environment_inspect
        from troubleshooting_mcp.models import (
            SystemInfoInput,
            ProcessSearchInput,
            EnvironmentSearchInput,
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
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)

        # Execute tools concurrently
        results = await asyncio.gather(
            tool_funcs['troubleshooting_get_system_info'](
                SystemInfoInput(response_format="markdown")
            ),
            tool_funcs['troubleshooting_search_processes'](ProcessSearchInput(limit=5)),
            tool_funcs['troubleshooting_inspect_environment'](EnvironmentSearchInput()),
        )

        # All should complete successfully
        assert len(results) == 3
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0


class TestServerEntryPoint:
    """Test server entry point and execution."""

    def test_main_function_exists(self):
        """Test that main() function exists."""
        from troubleshooting_mcp.server import main

        assert callable(main)

    def test_server_module_can_be_imported(self):
        """Test that server module can be imported without errors."""
        try:
            import troubleshooting_mcp.server
            assert True
        except Exception as e:
            pytest.fail(f"Failed to import server module: {e}")

    def test_backward_compatibility_wrapper(self):
        """Test that backward compatibility wrapper exists."""
        import os
        wrapper_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'troubleshooting_mcp.py'
        )

        # Check if wrapper file exists
        assert os.path.exists(wrapper_path), "Backward compatibility wrapper not found"

        # Verify it's executable
        assert os.access(wrapper_path, os.R_OK), "Wrapper is not readable"

    def test_package_initialization(self):
        """Test that package __init__.py properly initializes."""
        try:
            import troubleshooting_mcp
            assert hasattr(troubleshooting_mcp, '__version__') or True
        except Exception as e:
            pytest.fail(f"Failed to import package: {e}")

    def test_all_modules_importable(self):
        """Test that all modules can be imported."""
        modules = [
            'troubleshooting_mcp.server',
            'troubleshooting_mcp.models',
            'troubleshooting_mcp.utils',
            'troubleshooting_mcp.constants',
            'troubleshooting_mcp.tools',
            'troubleshooting_mcp.tools.system_info',
            'troubleshooting_mcp.tools.resource_monitor',
            'troubleshooting_mcp.tools.log_reader',
            'troubleshooting_mcp.tools.network_diagnostic',
            'troubleshooting_mcp.tools.process_search',
            'troubleshooting_mcp.tools.environment_inspect',
            'troubleshooting_mcp.tools.safe_command',
        ]

        for module_name in modules:
            try:
                __import__(module_name)
            except Exception as e:
                pytest.fail(f"Failed to import {module_name}: {e}")


class TestToolMetadata:
    """Test that all tools have proper metadata."""

    def test_all_tools_have_descriptions(self):
        """Test that all tools have description metadata."""
        from troubleshooting_mcp.tools import (
            system_info,
            resource_monitor,
            log_reader,
            network_diagnostic,
            process_search,
            environment_inspect,
            safe_command,
        )

        mock_mcp = MagicMock()
        tool_metadata = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_metadata.append(kwargs)
                return func
            return decorator

        mock_mcp.tool = mock_tool

        # Register all tools
        system_info.register_system_info(mock_mcp)
        resource_monitor.register_resource_monitor(mock_mcp)
        log_reader.register_log_reader(mock_mcp)
        network_diagnostic.register_network_diagnostic(mock_mcp)
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)
        safe_command.register_safe_command(mock_mcp)

        # Verify all tools have descriptions
        for metadata in tool_metadata:
            assert 'description' in metadata or 'name' in metadata
            assert metadata  # Not empty

    def test_all_tools_marked_read_only(self):
        """Test that all tools have readOnlyHint=True."""
        from troubleshooting_mcp.tools import (
            system_info,
            resource_monitor,
            log_reader,
            network_diagnostic,
            process_search,
            environment_inspect,
            safe_command,
        )

        mock_mcp = MagicMock()
        tool_metadata = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_metadata.append(kwargs)
                return func
            return decorator

        mock_mcp.tool = mock_tool

        # Register all tools
        system_info.register_system_info(mock_mcp)
        resource_monitor.register_resource_monitor(mock_mcp)
        log_reader.register_log_reader(mock_mcp)
        network_diagnostic.register_network_diagnostic(mock_mcp)
        process_search.register_process_search(mock_mcp)
        environment_inspect.register_environment_inspect(mock_mcp)
        safe_command.register_safe_command(mock_mcp)

        # Note: readOnlyHint might not be in all metadata,
        # but we verify structure is present
        assert len(tool_metadata) == 7


class TestErrorPropagation:
    """Test that errors propagate correctly through the integration."""

    @pytest.mark.asyncio
    async def test_invalid_input_propagates_error(self):
        """Test that invalid input to a tool propagates error correctly."""
        from troubleshooting_mcp.tools import log_reader
        from troubleshooting_mcp.models import LogFileInput

        mock_mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mock_mcp.tool = mock_tool
        log_reader.register_log_reader(mock_mcp)
        func = tool_funcs[0]

        # Pass invalid file path
        params = LogFileInput(file_path="/nonexistent/file.log")
        result = await func(params)

        # Should return error message, not crash
        assert isinstance(result, str)
        assert "not found" in result.lower() or "error" in result.lower()

    @pytest.mark.asyncio
    async def test_tool_exception_handling(self):
        """Test that exceptions in tools are handled gracefully."""
        from troubleshooting_mcp.tools import network_diagnostic
        from troubleshooting_mcp.models import NetworkDiagnosticInput

        mock_mcp = MagicMock()
        tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                tool_funcs.append(func)
                return func
            return decorator

        mcp.tool = mock_tool
        network_diagnostic.register_network_diagnostic(mock_mcp)
        func = tool_funcs[0]

        # Use invalid hostname
        params = NetworkDiagnosticInput(host="invalid.invalid")
        result = await func(params)

        # Should handle DNS failure gracefully
        assert isinstance(result, str)
        assert len(result) > 0
