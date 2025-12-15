
import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.troubleshooting_mcp.tools.log_reader import register_log_reader
from src.troubleshooting_mcp.models import LogFileInput

# Mock MCP for tool registration
class MockMCP:
    def __init__(self):
        self.tool_func = None

    def tool(self, name, annotations=None):
        def decorator(func):
            self.tool_func = func
            return func
        return decorator

@pytest.fixture
def log_reader_tool():
    mcp = MockMCP()
    register_log_reader(mcp)
    return mcp.tool_func

@pytest.mark.asyncio
async def test_log_reader_access_denied(log_reader_tool, tmp_path):
    # Create a secret file outside allowed directories
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("secret")

    # Try to read it
    params = LogFileInput(file_path=str(secret_file))
    result = await log_reader_tool(params)

    assert "Error: Security violation" in result
    assert "Access to" in result

@pytest.mark.asyncio
async def test_log_reader_traversal_attack(log_reader_tool):
    # Try to access /etc/passwd using traversal
    # Note: We rely on the fact that /etc/passwd exists on linux,
    # but the check happens before file existence check usually,
    # except our code resolves path first.

    # We need to construct a path that might look like it's inside allowed dir but traverses out
    # e.g. /var/log/../../etc/passwd

    params = LogFileInput(file_path="/var/log/../../etc/passwd")
    result = await log_reader_tool(params)

    assert "Error: Security violation" in result

@pytest.mark.asyncio
async def test_log_reader_allowed_access(log_reader_tool, tmp_path):
    # Mock ALLOWED_LOG_DIRS to include tmp_path
    with patch("src.troubleshooting_mcp.tools.log_reader.ALLOWED_LOG_DIRS", [str(tmp_path)]):
        # Create a log file inside tmp_path
        log_file = tmp_path / "app.log"
        log_file.write_text("log content")

        params = LogFileInput(file_path=str(log_file))
        result = await log_reader_tool(params)

        assert "log content" in result
        assert "Error: Security violation" not in result
