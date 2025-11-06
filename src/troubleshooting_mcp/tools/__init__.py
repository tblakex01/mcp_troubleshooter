"""
Individual diagnostic tools for the Troubleshooting MCP Server.
"""

from .environment_inspect import register_environment_inspect
from .log_reader import register_log_reader
from .network_diagnostic import register_network_diagnostic
from .process_search import register_process_search
from .resource_monitor import register_resource_monitor
from .safe_command import register_safe_command
from .system_info import register_system_info

__all__ = [
    "register_system_info",
    "register_resource_monitor",
    "register_log_reader",
    "register_network_diagnostic",
    "register_process_search",
    "register_environment_inspect",
    "register_safe_command",
]


def register_all_tools(mcp):
    """Register all diagnostic tools with the MCP server."""
    register_system_info(mcp)
    register_resource_monitor(mcp)
    register_log_reader(mcp)
    register_network_diagnostic(mcp)
    register_process_search(mcp)
    register_environment_inspect(mcp)
    register_safe_command(mcp)
