"""
Troubleshooting MCP Server

A Model Context Protocol (MCP) server that provides system troubleshooting and
diagnostic tools for developers and system administrators.
"""

__version__ = "1.0.0"
__author__ = "Troubleshooting MCP Server Contributors"
__license__ = "MIT"

from .server import mcp

__all__ = ["mcp"]
