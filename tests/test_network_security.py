import pytest
from pydantic import ValidationError

try:
    from troubleshooting_mcp.models import NetworkDiagnosticInput
except ImportError:
    from src.troubleshooting_mcp.models import NetworkDiagnosticInput

from src.troubleshooting_mcp.tools import network_diagnostic
from unittest.mock import MagicMock, patch
import asyncio

def test_block_local_hostnames():
    """Test that local hostnames are blocked during input validation."""
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="localhost", port=80)

    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="LOCALHOST", port=80)

    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="localhost.localdomain", port=80)

def test_block_internal_ips():
    """Test that internal IPs are blocked during input validation."""
    # Loopback
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="127.0.0.1", port=80)
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="::1", port=80)

    # Private
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="10.0.0.1", port=80)
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="192.168.1.1", port=80)
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="172.16.0.1", port=80)

    # Link-local (AWS Metadata)
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="169.254.169.254", port=80)

    # Multicast
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="224.0.0.1", port=80)

    # Unspecified
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="0.0.0.0", port=80)
    with pytest.raises(ValidationError, match="not allowed"):
        NetworkDiagnosticInput(host="::", port=80)

    # Valid external IP should pass
    NetworkDiagnosticInput(host="8.8.8.8", port=53)

@pytest.mark.asyncio
async def test_dns_rebinding_protection():
    """Test that dns resolution catching internal IPs prevents connection."""
    mcp = MagicMock()
    tool_funcs = []

    def mock_tool(*args, **kwargs):
        def decorator(func):
            tool_funcs.append(func)
            return func
        return decorator

    mcp.tool = mock_tool
    network_diagnostic.register_network_diagnostic(mcp)

    tool_func = tool_funcs[0]

    # We pass validation by using a non-local hostname, but mock socket.gethostbyname to return an internal IP
    params = NetworkDiagnosticInput(host="my-fake-external-domain.com", port=80)

    with patch("socket.gethostbyname", return_value="127.0.0.1"):
        result = await tool_func(params)
        assert "✗ **Security Error:** Connection Blocked" in result
        assert "restricted internal/private IP address (127.0.0.1)" in result

    with patch("socket.gethostbyname", return_value="169.254.169.254"):
        result = await tool_func(params)
        assert "✗ **Security Error:** Connection Blocked" in result
        assert "restricted internal/private IP address (169.254.169.254)" in result

    # External IP should not be blocked
    with patch("socket.gethostbyname", return_value="8.8.8.8"):
        # Just mock connect so it doesn't really connect
        with patch("socket.socket") as mock_socket:
            result = await tool_func(params)
            assert "✓ **DNS Resolution:** Success" in result
            assert "✗ **Security Error:** Connection Blocked" not in result
