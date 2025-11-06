#!/usr/bin/env python3
"""
Troubleshooting MCP Server - Backward Compatibility Entry Point

This file provides backward compatibility for users who have configured
Claude Desktop with the old single-file structure. It simply imports and
runs the modular server from the src package.

For new installations, you can use the package directly:
    python -m troubleshooting_mcp.server

Or install it and use the command:
    pip install -e .
    troubleshooting-mcp
"""

from src.troubleshooting_mcp.server import main

if __name__ == "__main__":
    main()
