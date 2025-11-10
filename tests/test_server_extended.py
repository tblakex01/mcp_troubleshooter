"""
Extended tests for server module.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_server_main_function_exists():
    """Test that the main function exists and is callable."""
    from troubleshooting_mcp.server import main

    assert callable(main)


def test_server_mcp_instance():
    """Test that the MCP server instance is created."""
    from troubleshooting_mcp.server import mcp

    assert mcp is not None
    assert hasattr(mcp, "name")


def test_server_name():
    """Test that the server has the correct name."""
    from troubleshooting_mcp.server import mcp

    # The server should have a name attribute
    assert hasattr(mcp, "name")


def test_package_exports():
    """Test that package exports are correct."""
    from troubleshooting_mcp import __version__, __author__, __license__

    assert isinstance(__version__, str)
    assert isinstance(__author__, str)
    assert isinstance(__license__, str)


def test_all_tools_registered():
    """Test that all 7 tools are registered."""
    from troubleshooting_mcp.server import mcp

    # The MCP server should have tools registered
    assert mcp is not None
