"""
Security tests for environment_inspect tool.
"""

import os
import json
from unittest.mock import MagicMock, patch
import pytest

from troubleshooting_mcp.models import EnvironmentSearchInput, ResponseFormat
from troubleshooting_mcp.tools import environment_inspect

class TestEnvironmentSecurity:
    """Tests for security controls in environment_inspect tool."""

    @pytest.mark.asyncio
    async def test_environment_variable_masking(self):
        """Test that sensitive environment variables are masked."""

        # Create a mock MCP server
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

        # Set sensitive environment variables
        sensitive_vars = {
            "MY_API_KEY": "super_secret_key_123",
            "DB_PASSWORD": "db_password_456",
            "AWS_SECRET_ACCESS_KEY": "aws_secret_789",
            "AUTH_TOKEN": "auth_token_abc",
            "PRIVATE_KEY": "private_key_xyz",
            "SSL_CERTIFICATE": "certificate_content",
            "PUBLIC_VAR": "public_value_123"
        }

        with patch.dict(os.environ, sensitive_vars):
            params = EnvironmentSearchInput(response_format=ResponseFormat.JSON)
            result = await func(params)

            # Parse result
            data = json.loads(result)
            env_vars = data["environment_variables"]

            # Check sensitive variables are masked
            assert env_vars["MY_API_KEY"] == "******** (masked for security)"
            assert env_vars["DB_PASSWORD"] == "******** (masked for security)"
            assert env_vars["AWS_SECRET_ACCESS_KEY"] == "******** (masked for security)"
            assert env_vars["AUTH_TOKEN"] == "******** (masked for security)"
            assert env_vars["PRIVATE_KEY"] == "******** (masked for security)"
            assert env_vars["SSL_CERTIFICATE"] == "******** (masked for security)"

            # Check non-sensitive variable is NOT masked
            assert env_vars["PUBLIC_VAR"] == "public_value_123"

    @pytest.mark.asyncio
    async def test_environment_variable_masking_false_positives(self):
        """Test that variables with sensitive substrings but no word boundaries are NOT masked."""

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

        # Variables that contain "KEY" but are not keys
        vars_to_test = {
            "KEYBOARD_LAYOUT": "us",
            "MONKEY_BUSINESS": "true",
            "DONKEY_KONG": "game",
            "AUTHORS": "John Doe",  # Contains AUTH but matches AUTHORS
            "SECRETARY": "Alice",    # Contains SECRET but matches SECRETARY
        }

        with patch.dict(os.environ, vars_to_test):
            params = EnvironmentSearchInput(response_format=ResponseFormat.JSON)
            result = await func(params)

            data = json.loads(result)
            env_vars = data["environment_variables"]

            # These should NOT be masked
            assert env_vars["KEYBOARD_LAYOUT"] == "us"
            assert env_vars["MONKEY_BUSINESS"] == "true"
            assert env_vars["DONKEY_KONG"] == "game"
            assert env_vars["AUTHORS"] == "John Doe"
            assert env_vars["SECRETARY"] == "Alice"

    @pytest.mark.asyncio
    async def test_environment_variable_masking_markdown(self):
        """Test that sensitive environment variables are masked in Markdown output."""

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

        with patch.dict(os.environ, {"API_KEY": "secret123", "NORMAL_VAR": "normal"}):
            params = EnvironmentSearchInput(response_format=ResponseFormat.MARKDOWN)
            result = await func(params)

            # Check masking in Markdown
            assert "******** (masked for security)" in result
            assert "secret123" not in result
            assert "normal" in result
