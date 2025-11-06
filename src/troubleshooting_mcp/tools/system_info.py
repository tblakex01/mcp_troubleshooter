"""
System Information Tool - Get comprehensive system details.
"""

import json
import platform
import sys

import psutil

from ..models import ResponseFormat, SystemInfoInput
from ..utils import format_bytes, format_timestamp, handle_error


def register_system_info(mcp):
    """Register the system information tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_get_system_info",
        annotations={
            "title": "Get System Information",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_get_system_info(params: SystemInfoInput) -> str:
        """Get comprehensive system information including OS, hardware, and software versions.

        This tool provides detailed information about the system including operating system details,
        CPU architecture, memory capacity, Python version, and installed software versions.
        It does NOT modify the system in any way.

        Args:
            params (SystemInfoInput): Validated input parameters containing:
                - response_format (ResponseFormat): Output format ('markdown' or 'json')

        Returns:
            str: System information in the requested format

            Markdown format: Formatted with headers and sections
            JSON format: Structured data with all system details

        Examples:
            - Use when: "What operating system is this server running?"
            - Use when: "Show me the system specs"
            - Use when: "What version of Python is installed?"

        Error Handling:
            - Returns formatted error message if system info cannot be retrieved
            - Handles permission errors gracefully
        """
        try:
            # Gather system information
            uname = platform.uname()
            boot_time = psutil.boot_time()

            # Get Python version and path
            python_version = sys.version
            python_executable = sys.executable

            # Get CPU info
            cpu_count = psutil.cpu_count(logical=True)
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()

            # Get memory info
            mem = psutil.virtual_memory()

            # Get disk info
            disk = psutil.disk_usage("/")

            info = {
                "system": uname.system,
                "node_name": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
                "processor": uname.processor,
                "boot_time": format_timestamp(boot_time),
                "python_version": python_version.split("\n")[0],
                "python_executable": python_executable,
                "cpu": {
                    "physical_cores": cpu_count_physical,
                    "logical_cores": cpu_count,
                    "max_frequency": f"{cpu_freq.max:.2f} MHz" if cpu_freq else "N/A",
                    "current_frequency": f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A",
                },
                "memory": {
                    "total": format_bytes(mem.total),
                    "available": format_bytes(mem.available),
                    "percent_used": f"{mem.percent}%",
                },
                "disk": {
                    "total": format_bytes(disk.total),
                    "used": format_bytes(disk.used),
                    "free": format_bytes(disk.free),
                    "percent_used": f"{(disk.used / disk.total * 100):.1f}%",
                },
            }

            if params.response_format == ResponseFormat.MARKDOWN:
                lines = ["# System Information", ""]
                lines.append(f"**Operating System:** {info['system']} {info['release']}")
                lines.append(f"**Hostname:** {info['node_name']}")
                lines.append(f"**Architecture:** {info['machine']}")
                lines.append(f"**Processor:** {info['processor']}")
                lines.append(f"**Boot Time:** {info['boot_time']}")
                lines.append("")

                lines.append("## Python Environment")
                lines.append(f"**Version:** {info['python_version']}")
                lines.append(f"**Executable:** {info['python_executable']}")
                lines.append("")

                lines.append("## CPU")
                lines.append(f"**Physical Cores:** {info['cpu']['physical_cores']}")
                lines.append(f"**Logical Cores:** {info['cpu']['logical_cores']}")
                lines.append(f"**Max Frequency:** {info['cpu']['max_frequency']}")
                lines.append(f"**Current Frequency:** {info['cpu']['current_frequency']}")
                lines.append("")

                lines.append("## Memory")
                lines.append(f"**Total:** {info['memory']['total']}")
                lines.append(f"**Available:** {info['memory']['available']}")
                lines.append(f"**Usage:** {info['memory']['percent_used']}")
                lines.append("")

                lines.append("## Disk (Root)")
                lines.append(f"**Total:** {info['disk']['total']}")
                lines.append(f"**Used:** {info['disk']['used']}")
                lines.append(f"**Free:** {info['disk']['free']}")
                lines.append(f"**Usage:** {info['disk']['percent_used']}")

                return "\n".join(lines)
            else:
                return json.dumps(info, indent=2)

        except Exception as e:
            return handle_error(e)
