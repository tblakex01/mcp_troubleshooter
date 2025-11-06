"""
Process Search Tool - Search for running processes.
"""

import json

import psutil

from ..models import ProcessSearchInput, ResponseFormat
from ..utils import check_character_limit, format_bytes, handle_error


def register_process_search(mcp):
    """Register the process search tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_search_processes",
        annotations={
            "title": "Search Running Processes",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_search_processes(params: ProcessSearchInput) -> str:
        """Search for running processes by name pattern with resource usage details.

        This tool searches through currently running processes and returns detailed
        information including PID, CPU usage, memory usage, and command line. If no
        pattern is provided, it returns a list of all processes sorted by resource usage.

        Args:
            params (ProcessSearchInput): Validated input parameters containing:
                - pattern (Optional[str]): Search pattern for process name (case-insensitive)
                - limit (Optional[int]): Maximum processes to return (default: 20, max: 100)
                - response_format (ResponseFormat): Output format ('markdown' or 'json')

        Returns:
            str: Process information in the requested format

            Success response includes for each process:
            - PID (Process ID)
            - Process name
            - CPU usage percentage
            - Memory usage (RSS)
            - Status (running, sleeping, etc.)
            - Command line

            Error response:
            - "No processes found matching 'pattern'" if no matches

        Examples:
            - Use when: "Is nginx running?"
            - Use when: "Show me all Python processes"
            - Use when: "Find processes using the most memory"
            - Use when: "List all active processes"
            - Don't use when: You want to kill processes (use system tools directly)

        Error Handling:
            - Handles permission errors when accessing process information
            - Skips processes that terminate during enumeration
            - Returns empty list if no processes match pattern
        """
        try:
            processes = []

            # Iterate through all running processes
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_info", "status", "cmdline"]
            ):
                try:
                    pinfo = proc.info

                    # Apply pattern filter if provided
                    if params.pattern:
                        pattern_lower = params.pattern.lower()
                        name_match = pattern_lower in pinfo["name"].lower()
                        cmdline_match = False
                        if pinfo["cmdline"]:
                            cmdline_str = " ".join(pinfo["cmdline"]).lower()
                            cmdline_match = pattern_lower in cmdline_str

                        if not (name_match or cmdline_match):
                            continue

                    # Get memory in bytes
                    mem_bytes = pinfo["memory_info"].rss if pinfo["memory_info"] else 0

                    processes.append(
                        {
                            "pid": pinfo["pid"],
                            "name": pinfo["name"],
                            "cpu_percent": pinfo["cpu_percent"] or 0.0,
                            "memory_bytes": mem_bytes,
                            "memory_formatted": format_bytes(mem_bytes),
                            "status": pinfo["status"],
                            "cmdline": (
                                " ".join(pinfo["cmdline"][:3])
                                if pinfo["cmdline"]
                                else pinfo["name"]
                            ),
                        }
                    )

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            if not processes:
                if params.pattern:
                    return f"No processes found matching '{params.pattern}'"
                return "No processes found"

            # Sort by CPU usage (descending)
            processes.sort(key=lambda x: x["cpu_percent"], reverse=True)

            # Limit results
            processes = processes[: params.limit]

            if params.response_format == ResponseFormat.MARKDOWN:
                lines = ["# Running Processes", ""]

                if params.pattern:
                    lines.append(f"**Filter:** '{params.pattern}'")
                lines.append(f"**Count:** {len(processes)} (limit: {params.limit})")
                lines.append("")

                for proc in processes:
                    lines.append(f"## {proc['name']} (PID: {proc['pid']})")
                    lines.append(f"- **CPU:** {proc['cpu_percent']:.1f}%")
                    lines.append(f"- **Memory:** {proc['memory_formatted']}")
                    lines.append(f"- **Status:** {proc['status']}")
                    lines.append(f"- **Command:** `{proc['cmdline']}`")
                    lines.append("")

                result = "\n".join(lines)
                return check_character_limit(result, "process list")
            else:
                data = {
                    "total_found": len(processes),
                    "limit": params.limit,
                    "filter": params.pattern,
                    "processes": processes,
                }
                return json.dumps(data, indent=2)

        except Exception as e:
            return handle_error(e)
