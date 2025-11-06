#!/usr/bin/env python3
"""
Troubleshooting MCP Server - Main Entry Point

A Model Context Protocol (MCP) server that provides system troubleshooting and
diagnostic tools for developers and system administrators.
"""

from mcp.server.fastmcp import FastMCP

from .tools import register_all_tools

# Initialize the MCP server
mcp = FastMCP("troubleshooting_mcp")

# Register all diagnostic tools
register_all_tools(mcp)


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()
