
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
        "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE", # Should NOT be masked (matches KEY but not KEY$) -> wait, regex is (?:^|_)KEY$ matches KEY_ID? No.
        "AUTH_TOKEN": "auth_token_value",
        "DB_CREDENTIALS": "db_password",
        "MONKEY_KEY": "banana_key", # Should be masked (ends in KEY)
        "AUTH_METHOD": "Basic", # Should NOT be masked (starts with AUTH but not AUTH$)
        "SSH_PRIVATE_KEY": "private_key_content",
        "MY_CERT": "cert_content",
        "KEYBOARD_LAYOUT": "US" # Should NOT be masked
    })
    def test_environment_masking(self):
        # We need to run the async function
        import asyncio

        async def run_test():
            params = EnvironmentSearchInput()
            result = await self.func(params)
            return result

        result = asyncio.run(run_test())

        # Helper to check masking
        def assert_masked(key, original_value):
            self.assertIn(key, result, f"Key {key} missing from output")
            self.assertNotIn(original_value, result, f"Value for {key} was NOT masked!")
            self.assertIn("******** (masked)", result, f"Masked placeholder missing for {key}")

        def assert_not_masked(key, original_value):
            self.assertIn(key, result, f"Key {key} missing from output")
            self.assertIn(original_value, result, f"Value for {key} WAS masked incorrectly!")

        # --- Check Masked Items ---
        assert_masked("MY_SECRET_PASSWORD", "secret_password")
        assert_masked("API_KEY", "123456789")
        assert_masked("AWS_SECRET_ACCESS_KEY", "aws_secret")
        assert_masked("AUTH_TOKEN", "auth_token_value")
        assert_masked("DB_CREDENTIALS", "db_password")
        assert_masked("MONKEY_KEY", "banana_key")
        assert_masked("SSH_PRIVATE_KEY", "private_key_content")
        assert_masked("MY_CERT", "cert_content")

        # --- Check Non-Masked Items ---
        assert_not_masked("MY_PUBLIC_VAR", "public_value")
        assert_not_masked("AUTH_METHOD", "Basic")
        assert_not_masked("KEYBOARD_LAYOUT", "US")
        assert_not_masked("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")

if __name__ == "__main__":
    unittest.main()
