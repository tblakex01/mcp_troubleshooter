"""
Resource Monitoring Tool - Monitor system resources in real-time.
"""

import json

import psutil

from ..models import ResourceMonitorInput, ResponseFormat
from ..utils import format_bytes, handle_error


def register_resource_monitor(mcp):
    """Register the resource monitoring tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_monitor_resources",
        annotations={
            "title": "Monitor System Resources",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_monitor_resources(params: ResourceMonitorInput) -> str:
        """Monitor current system resource usage including CPU, memory, and disk.

        This tool provides real-time snapshots of system resource utilization. It shows
        current CPU usage, memory consumption, swap usage, and disk I/O statistics.
        Results may vary between calls as they reflect current system state.

        Args:
            params (ResourceMonitorInput): Validated input parameters containing:
                - include_per_cpu (Optional[bool]): Include per-CPU statistics (default: False)
                - response_format (ResponseFormat): Output format ('markdown' or 'json')

        Returns:
            str: Resource monitoring data in the requested format

            Success response includes:
            - CPU usage (overall and per-core if requested)
            - Memory usage (physical and swap)
            - Disk I/O statistics
            - Network I/O statistics

        Examples:
            - Use when: "What's the current CPU usage?"
            - Use when: "Is the system running out of memory?"
            - Use when: "Show me resource utilization"
            - Don't use when: You need historical data (this shows current snapshot only)

        Error Handling:
            - Returns formatted error message if resource data cannot be retrieved
            - Handles permission errors for restricted metrics
        """
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = (
                psutil.cpu_percent(interval=1, percpu=True) if params.include_per_cpu else None
            )

            # Get memory info
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # Get disk I/O
            disk_io = psutil.disk_io_counters()

            # Get network I/O
            net_io = psutil.net_io_counters()

            data = {
                "cpu": {
                    "overall_percent": cpu_percent,
                    "per_core_percent": cpu_per_core if params.include_per_cpu else None,
                },
                "memory": {
                    "total": mem.total,
                    "available": mem.available,
                    "used": mem.used,
                    "percent": mem.percent,
                    "total_formatted": format_bytes(mem.total),
                    "used_formatted": format_bytes(mem.used),
                    "available_formatted": format_bytes(mem.available),
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent,
                    "total_formatted": format_bytes(swap.total),
                    "used_formatted": format_bytes(swap.used),
                    "free_formatted": format_bytes(swap.free),
                },
                "disk_io": (
                    {
                        "read_bytes": format_bytes(disk_io.read_bytes),
                        "write_bytes": format_bytes(disk_io.write_bytes),
                        "read_count": disk_io.read_count,
                        "write_count": disk_io.write_count,
                    }
                    if disk_io
                    else None
                ),
                "network_io": (
                    {
                        "bytes_sent": format_bytes(net_io.bytes_sent),
                        "bytes_recv": format_bytes(net_io.bytes_recv),
                        "packets_sent": net_io.packets_sent,
                        "packets_recv": net_io.packets_recv,
                    }
                    if net_io
                    else None
                ),
            }

            if params.response_format == ResponseFormat.MARKDOWN:
                lines = ["# System Resource Monitor", ""]

                lines.append("## CPU Usage")
                lines.append(f"**Overall:** {data['cpu']['overall_percent']}%")
                if params.include_per_cpu and cpu_per_core:
                    lines.append("\n**Per-Core Usage:**")
                    for i, usage in enumerate(cpu_per_core):
                        lines.append(f"- Core {i}: {usage}%")
                lines.append("")

                lines.append("## Memory Usage")
                lines.append(f"**Total:** {data['memory']['total_formatted']}")
                lines.append(
                    f"**Used:** {data['memory']['used_formatted']} ({data['memory']['percent']}%)"
                )
                lines.append(f"**Available:** {data['memory']['available_formatted']}")
                lines.append("")

                lines.append("## Swap Usage")
                lines.append(f"**Total:** {data['swap']['total_formatted']}")
                lines.append(
                    f"**Used:** {data['swap']['used_formatted']} ({data['swap']['percent']}%)"
                )
                lines.append(f"**Free:** {data['swap']['free_formatted']}")
                lines.append("")

                if data["disk_io"]:
                    lines.append("## Disk I/O (since boot)")
                    lines.append(
                        f"**Read:** {data['disk_io']['read_bytes']} ({data['disk_io']['read_count']} operations)"
                    )
                    lines.append(
                        f"**Write:** {data['disk_io']['write_bytes']} ({data['disk_io']['write_count']} operations)"
                    )
                    lines.append("")

                if data["network_io"]:
                    lines.append("## Network I/O (since boot)")
                    lines.append(
                        f"**Sent:** {data['network_io']['bytes_sent']} ({data['network_io']['packets_sent']} packets)"
                    )
                    lines.append(
                        f"**Received:** {data['network_io']['bytes_recv']} ({data['network_io']['packets_recv']} packets)"
                    )

                return "\n".join(lines)
            else:
                return json.dumps(data, indent=2)

        except Exception as e:
            return handle_error(e)
