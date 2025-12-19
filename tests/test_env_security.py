
import os
import pytest
from src.troubleshooting_mcp.tools.environment_inspect import register_environment_inspect
from src.troubleshooting_mcp.models import EnvironmentSearchInput, ResponseFormat
from unittest.mock import MagicMock

class MockMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, name, annotations=None):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

@pytest.mark.asyncio
async def test_env_var_masking():
    # Set a sensitive environment variable
    os.environ["TEST_SECRET_API_KEY"] = "super_secret_value_12345"
    os.environ["NORMAL_VAR"] = "normal_value"

    mcp = MockMCP()
    register_environment_inspect(mcp)

    tool_func = mcp.tools["troubleshooting_inspect_environment"]

    # Call the tool
    params = EnvironmentSearchInput(pattern="TEST_SECRET", response_format=ResponseFormat.JSON)
    result = await tool_func(params)

    # Verify the masking
    assert "******** [MASKED FOR SECURITY] ********" in result
    assert "super_secret_value_12345" not in result
    assert "TEST_SECRET_API_KEY" in result

    # Verify normal variable is not masked
    params = EnvironmentSearchInput(pattern="NORMAL_VAR", response_format=ResponseFormat.JSON)
    result = await tool_func(params)
    assert "normal_value" in result

    # Cleanup
    del os.environ["TEST_SECRET_API_KEY"]
    del os.environ["NORMAL_VAR"]
