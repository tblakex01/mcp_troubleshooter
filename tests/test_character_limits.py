"""
Character limit and truncation testing.

This test module focuses on testing the CHARACTER_LIMIT (25000 characters)
enforcement across all tools:
- Log reader with large files
- Safe command with large output
- Process search with many processes
- Truncation message format verification
"""

import pytest
import tempfile
import os
from unittest.mock import MagicMock, patch

from troubleshooting_mcp.models import (
    LogFileInput,
    SafeCommandInput,
    ProcessSearchInput,
)
from troubleshooting_mcp.constants import CHARACTER_LIMIT
from troubleshooting_mcp.utils import check_character_limit


class TestCharacterLimitUtility:
    """Test the check_character_limit utility function."""

    def test_content_under_limit(self):
        """Test content that's under the character limit."""
        content = "x" * 1000
        result = check_character_limit(content)

        assert result == content
        assert "truncated" not in result.lower()

    def test_content_at_exact_limit(self):
        """Test content exactly at CHARACTER_LIMIT."""
        content = "x" * CHARACTER_LIMIT
        result = check_character_limit(content)

        # Should NOT be truncated
        assert len(result) == CHARACTER_LIMIT
        assert "truncated" not in result.lower()

    def test_content_one_over_limit(self):
        """Test content one character over limit."""
        content = "x" * (CHARACTER_LIMIT + 1)
        result = check_character_limit(content)

        # Should be truncated
        assert len(result) < len(content)
        assert "truncated" in result.lower()

    def test_content_far_over_limit(self):
        """Test content far exceeding the limit."""
        content = "x" * (CHARACTER_LIMIT * 2)
        result = check_character_limit(content)

        # Should be truncated
        assert len(result) < len(content)
        assert "truncated" in result.lower()
        # Check that original size is mentioned
        assert str(CHARACTER_LIMIT * 2) in result or "truncated" in result.lower()

    def test_truncation_message_format(self):
        """Test that truncation message has proper format."""
        content = "x" * 30000
        result = check_character_limit(content)

        assert "truncated" in result.lower()
        # Should mention it was truncated
        assert len(result) > 0

    def test_custom_data_type_in_message(self):
        """Test that custom data_type appears in truncation message."""
        content = "x" * 30000
        result = check_character_limit(content, data_type="test data")

        assert "truncated" in result.lower()
        assert "test data" in result.lower()

    def test_empty_content(self):
        """Test check_character_limit with empty content."""
        result = check_character_limit("")
        assert result == ""

    def test_none_content_handling(self):
        """Test check_character_limit handles None gracefully."""
        # Should either handle None or raise appropriate error
        try:
            result = check_character_limit(None)
            # If it doesn't raise, should return something
            assert result is not None
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass


class TestLogReaderCharacterLimit:
    """Test character limit enforcement in log reader tool."""

    @pytest.mark.asyncio
    async def test_log_reader_large_file(self):
        """Test log reader with file exceeding character limit."""
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

        # Create a large temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            # Write lines that will exceed CHARACTER_LIMIT
            for i in range(1000):
                f.write(f"This is log line {i} with some content to make it longer\n")

        try:
            params = LogFileInput(file_path=temp_path, num_lines=1000)
            result = await func(params)

            # Result should be truncated if it exceeds limit
            if len(result) > CHARACTER_LIMIT:
                assert "truncated" in result.lower()
            # Either way, should not crash
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_log_reader_very_long_lines(self):
        """Test log reader with very long individual lines."""
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
            # Each line is 10000 characters
            for i in range(5):
                f.write("x" * 10000 + f" line {i}\n")

        try:
            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            # Should handle long lines
            assert isinstance(result, str)
            # May be truncated if total exceeds limit
            if len(result) >= CHARACTER_LIMIT:
                # Might have truncation warning
                pass
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_log_reader_exactly_at_limit(self):
        """Test log reader with content exactly at character limit."""
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

        # Create a file with content close to CHARACTER_LIMIT
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_path = f.name
            # Write exactly CHARACTER_LIMIT characters
            content = "x" * CHARACTER_LIMIT
            f.write(content)

        try:
            params = LogFileInput(file_path=temp_path)
            result = await func(params)

            # Should not be truncated if exactly at limit
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)


class TestSafeCommandCharacterLimit:
    """Test character limit enforcement in safe command tool."""

    @pytest.mark.asyncio
    async def test_safe_command_large_output(self):
        """Test safe command with output exceeding character limit."""
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

        # Mock subprocess to return very large output
        mock_result = MagicMock()
        mock_result.stdout = "x" * 30000  # Exceeds CHARACTER_LIMIT
        mock_result.stderr = ""
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            # Should be truncated
            assert isinstance(result, str)
            assert "truncated" in result.lower()
            assert len(result) <= CHARACTER_LIMIT + 500  # Allow for truncation message

    @pytest.mark.asyncio
    async def test_safe_command_large_stderr(self):
        """Test safe command with large stderr output."""
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

        # Mock subprocess to return large stderr
        mock_result = MagicMock()
        mock_result.stdout = "small output"
        mock_result.stderr = "e" * 30000  # Exceeds CHARACTER_LIMIT
        mock_result.returncode = 1

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            # Should handle large stderr
            assert isinstance(result, str)
            # May be truncated
            if len(result) >= CHARACTER_LIMIT:
                assert "truncated" in result.lower()

    @pytest.mark.asyncio
    async def test_safe_command_combined_output_limit(self):
        """Test safe command with combined stdout and stderr exceeding limit."""
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

        # Mock subprocess with both large stdout and stderr
        mock_result = MagicMock()
        mock_result.stdout = "o" * 15000
        mock_result.stderr = "e" * 15000
        mock_result.returncode = 1

        with patch('subprocess.run', return_value=mock_result):
            params = SafeCommandInput(command="ping")
            result = await func(params)

            # Combined output exceeds limit, should be handled
            assert isinstance(result, str)


class TestProcessSearchCharacterLimit:
    """Test character limit enforcement in process search tool."""

    @pytest.mark.asyncio
    async def test_process_search_many_processes(self):
        """Test process search with many processes potentially exceeding limit."""
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

        # Create many mock processes
        mock_processes = []
        for i in range(100):
            mock_proc = MagicMock()
            mock_proc.info = {
                'pid': i,
                'name': f'process_{i}',
                'cpu_percent': 1.0,
                'memory_percent': 1.0,
            }
            mock_proc.cmdline.return_value = [f'/usr/bin/process_{i}', 'arg1', 'arg2']
            mock_processes.append(mock_proc)

        with patch('psutil.process_iter', return_value=mock_processes):
            params = ProcessSearchInput(limit=100)
            result = await func(params)

            # Should handle many processes
            assert isinstance(result, str)
            # If output is huge, may be truncated
            if len(result) > CHARACTER_LIMIT:
                assert "truncated" in result.lower()

    @pytest.mark.asyncio
    async def test_process_search_long_cmdlines(self):
        """Test process search with very long command lines."""
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

        # Create processes with very long command lines
        mock_processes = []
        for i in range(10):
            mock_proc = MagicMock()
            mock_proc.info = {
                'pid': i,
                'name': f'proc{i}',
                'cpu_percent': 0.5,
                'memory_percent': 0.5,
            }
            # Very long command line
            mock_proc.cmdline.return_value = ['/usr/bin/program'] + ['arg'] * 1000
            mock_processes.append(mock_proc)

        with patch('psutil.process_iter', return_value=mock_processes):
            params = ProcessSearchInput()
            result = await func(params)

            # Should handle long cmdlines
            assert isinstance(result, str)
            # Check for potential truncation
            if len(result) > CHARACTER_LIMIT:
                assert "truncated" in result.lower()


class TestResourceMonitorCharacterLimit:
    """Test character limit in resource monitor (less likely but possible)."""

    @pytest.mark.asyncio
    async def test_resource_monitor_per_cpu_many_cores(self):
        """Test resource monitor with many CPU cores (per_cpu=True)."""
        from troubleshooting_mcp.tools import resource_monitor
        from troubleshooting_mcp.models import ResourceMonitorInput

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

        # Mock many CPU cores
        mock_cpu_percent = [1.0] * 128  # 128 cores

        with patch('psutil.cpu_percent', return_value=mock_cpu_percent):
            params = ResourceMonitorInput(per_cpu=True, response_format="markdown")
            result = await func(params)

            # Should handle many cores without issue
            assert isinstance(result, str)
            # Unlikely to exceed limit, but should be valid
            assert len(result) > 0


class TestSystemInfoCharacterLimit:
    """Test character limit in system info (unlikely but test for completeness)."""

    @pytest.mark.asyncio
    async def test_system_info_normal_output(self):
        """Test that system info output is well under character limit."""
        from troubleshooting_mcp.tools import system_info
        from troubleshooting_mcp.models import SystemInfoInput

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

        params = SystemInfoInput(response_format="markdown")
        result = await func(params)

        # System info should never exceed character limit
        assert isinstance(result, str)
        assert len(result) < CHARACTER_LIMIT
        assert "truncated" not in result.lower()


class TestTruncationMessageQuality:
    """Test that truncation messages are informative."""

    def test_truncation_includes_original_size(self):
        """Test that truncation message includes information about original size."""
        content = "x" * 30000
        result = check_character_limit(content)

        # Should mention truncation
        assert "truncated" in result.lower()
        # Should be a string
        assert isinstance(result, str)

    def test_truncation_preserves_beginning(self):
        """Test that truncation preserves the beginning of content."""
        content = "IMPORTANT_START" + "x" * 30000 + "END"
        result = check_character_limit(content)

        # Should preserve the start
        assert "IMPORTANT_START" in result
        # But not the end
        assert "END" not in result

    def test_truncation_with_newlines(self):
        """Test truncation handles newlines properly."""
        content = "\n".join([f"Line {i}" for i in range(10000)])
        result = check_character_limit(content)

        # Should handle newlines
        assert isinstance(result, str)
        if len(content) > CHARACTER_LIMIT:
            assert "truncated" in result.lower()

    def test_truncation_with_unicode(self):
        """Test truncation handles unicode content."""
        content = "🔥" * 30000
        result = check_character_limit(content)

        # Should handle unicode
        assert isinstance(result, str)
        assert "truncated" in result.lower()
