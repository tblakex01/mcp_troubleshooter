
import unittest
from unittest.mock import MagicMock, patch
import pytest
from troubleshooting_mcp.tools import process_search
from troubleshooting_mcp.models import ProcessSearchInput, ResponseFormat

class TestProcessSearchSecurity:
    @pytest.mark.asyncio
    async def test_process_search_masks_secrets(self):
        """Test that process search masks secrets in command line arguments."""

        # Mock process with sensitive command line
        mock_proc = MagicMock()
        mock_proc.info = {
            "pid": 1234,
            "name": "java",
            "cpu_percent": 1.0,
            "memory_info": MagicMock(rss=1024*1024),
            "status": "running",
            "cmdline": ["java", "-Dpassword=SuperSecretPassword123", "-jar", "app.jar"]
        }

        # Setup MCP mock
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

        # Mock psutil.process_iter
        with patch('psutil.process_iter', return_value=[mock_proc]):
            params = ProcessSearchInput(pattern="java")
            result = await func(params)

        # Assertions
        assert "SuperSecretPassword123" not in result
        assert "***" in result or "MASKED" in result
