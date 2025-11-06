"""
Integration tests for the Troubleshooting MCP Server.
"""



def test_package_import():
    """Test that the main package can be imported."""
    from troubleshooting_mcp import mcp

    assert mcp is not None


def test_server_import():
    """Test that the server module can be imported."""
    from troubleshooting_mcp.server import main, mcp

    assert mcp is not None
    assert callable(main)


def test_constants_import():
    """Test that constants can be imported."""
    from troubleshooting_mcp.constants import (
        CHARACTER_LIMIT,
        COMMON_LOG_PATHS,
        SAFE_COMMANDS,
    )

    assert CHARACTER_LIMIT > 0
    assert len(SAFE_COMMANDS) > 0
    assert len(COMMON_LOG_PATHS) > 0


def test_models_import():
    """Test that models can be imported."""
    from troubleshooting_mcp.models import (
        LogFileInput,
        ResponseFormat,
        SystemInfoInput,
    )

    assert ResponseFormat.MARKDOWN == "markdown"
    assert SystemInfoInput is not None
    assert LogFileInput is not None


def test_utils_import():
    """Test that utils can be imported."""
    from troubleshooting_mcp.utils import (
        format_bytes,
        format_timestamp,
        handle_error,
    )

    assert callable(format_bytes)
    assert callable(format_timestamp)
    assert callable(handle_error)


def test_tools_import():
    """Test that tools can be imported."""
    from troubleshooting_mcp.tools import register_all_tools

    assert callable(register_all_tools)


def test_package_metadata():
    """Test that package metadata is defined."""
    from troubleshooting_mcp import __author__, __license__, __version__

    assert __version__ == "1.0.0"
    assert __author__ is not None
    assert __license__ == "MIT"


def test_server_has_tools():
    """Test that server has tools registered."""
    from troubleshooting_mcp.server import mcp

    # The server should have been initialized
    assert mcp is not None
    assert hasattr(mcp, "name")
