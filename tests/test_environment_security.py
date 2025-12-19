
import os
import unittest
from unittest.mock import MagicMock, patch

from src.troubleshooting_mcp.models import EnvironmentSearchInput
from src.troubleshooting_mcp.tools import environment_inspect

class TestEnvironmentSecurity(unittest.TestCase):
    def setUp(self):
        self.mcp = MagicMock()
        self.tool_funcs = []

        def mock_tool(*args, **kwargs):
            def decorator(func):
                self.tool_funcs.append(func)
                return func
            return decorator

        self.mcp.tool = mock_tool
        environment_inspect.register_environment_inspect(self.mcp)
        self.func = self.tool_funcs[0]

    @patch.dict(os.environ, {
        "MY_PUBLIC_VAR": "public_value",
        "MY_SECRET_PASSWORD": "secret_password",
        "API_KEY": "123456789",
        "AWS_SECRET_ACCESS_KEY": "aws_secret",
        "AUTH_TOKEN": "auth_token_value",
        "DB_CREDENTIALS": "db_password"
    })
    def test_environment_masking(self):
        # We need to run the async function
        import asyncio

        async def run_test():
            params = EnvironmentSearchInput()
            result = await self.func(params)
            return result

        result = asyncio.run(run_test())

        # Check that non-sensitive values are present
        self.assertIn("MY_PUBLIC_VAR", result)
        self.assertIn("public_value", result)

        # Check that sensitive keys are present but values are masked
        self.assertIn("MY_SECRET_PASSWORD", result)
        self.assertNotIn("secret_password", result)
        self.assertIn("******** (masked)", result)

        self.assertIn("API_KEY", result)
        self.assertNotIn("123456789", result)

        self.assertIn("AWS_SECRET_ACCESS_KEY", result)
        self.assertNotIn("aws_secret", result)

        self.assertIn("AUTH_TOKEN", result)
        self.assertNotIn("auth_token_value", result)

        self.assertIn("DB_CREDENTIALS", result)
        self.assertNotIn("db_password", result)

if __name__ == "__main__":
    unittest.main()
