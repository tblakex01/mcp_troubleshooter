"""
Log File Reader Tool - Read and analyze system log files.
"""

import os
from pathlib import Path

from ..constants import COMMON_LOG_PATHS
from ..models import LogFileInput
from ..utils import check_character_limit, format_bytes, format_timestamp, handle_error


def register_log_reader(mcp):
    """Register the log file reader tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_read_log_file",
        annotations={
            "title": "Read Log Files",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_read_log_file(params: LogFileInput) -> str:
        """Read and tail system log files with optional filtering.

        This tool can read the last N lines from log files (similar to 'tail' command)
        and optionally filter entries using a search pattern. If no file path is provided,
        it lists common log file locations on the system.

        Args:
            params (LogFileInput): Validated input parameters containing:
                - file_path (Optional[str]): Path to log file (if None, lists common locations)
                - lines (Optional[int]): Number of lines to read from end (default: 50, max: 1000)
                - search_pattern (Optional[str]): Optional pattern to filter log entries

        Returns:
            str: Log file contents or list of common log locations

            When file_path is provided: Last N lines of the file (optionally filtered)
            When file_path is None: List of common log file paths on the system

        Examples:
            - Use when: "Show me the last 100 lines of /var/log/syslog"
            - Use when: "Check nginx error logs for issues"
            - Use when: "Search auth.log for 'failed password' entries"
            - Use when: "What log files are available?"

        Error Handling:
            - Returns "Error: Permission denied" if log file is not readable
            - Returns "Error: File not found" if log path doesn't exist
            - Handles binary files gracefully with appropriate error message
        """
        try:
            # If no file path provided, list common log locations
            if not params.file_path:
                lines = ["# Common Log File Locations", ""]
                lines.append("## Available Logs")

                found_logs = []
                for log_path in COMMON_LOG_PATHS:
                    if os.path.exists(log_path) and os.path.isfile(log_path):
                        try:
                            size = os.path.getsize(log_path)
                            mtime = os.path.getmtime(log_path)
                            found_logs.append(
                                {
                                    "path": log_path,
                                    "size": format_bytes(size),
                                    "modified": format_timestamp(mtime),
                                    "readable": os.access(log_path, os.R_OK),
                                }
                            )
                        except (PermissionError, OSError):
                            found_logs.append(
                                {
                                    "path": log_path,
                                    "size": "N/A",
                                    "modified": "N/A",
                                    "readable": False,
                                }
                            )

                if found_logs:
                    for log in found_logs:
                        status = "✓" if log["readable"] else "✗"
                        lines.append(f"{status} **{log['path']}**")
                        lines.append(f"  - Size: {log['size']}")
                        lines.append(f"  - Modified: {log['modified']}")
                        lines.append("")
                else:
                    lines.append("No common log files found on this system.")

                lines.append("\n*Use file_path parameter to read a specific log file*")
                return "\n".join(lines)

            # Validate file path
            log_file = Path(params.file_path)
            if not log_file.exists():
                return f"Error: Log file not found: {params.file_path}"

            if not log_file.is_file():
                return f"Error: Path is not a file: {params.file_path}"

            if not os.access(log_file, os.R_OK):
                return f"Error: Permission denied. Cannot read file: {params.file_path}"

            # Read the last N lines
            with open(log_file, errors="ignore") as f:
                # For large files, use efficient tail-like approach
                lines_list = []
                try:
                    # Try to seek to end and read backwards for efficiency
                    f.seek(0, 2)  # Seek to end
                    file_size = f.tell()

                    if file_size > 0:
                        # Read in chunks from the end
                        chunk_size = 8192
                        offset = min(chunk_size * params.lines, file_size)
                        f.seek(max(0, file_size - offset))
                        lines_list = f.readlines()[-params.lines :]
                except Exception:
                    # Fallback: read entire file
                    f.seek(0)
                    lines_list = f.readlines()[-params.lines :]

            # Apply search filter if provided
            if params.search_pattern:
                pattern = params.search_pattern.lower()
                lines_list = [line for line in lines_list if pattern in line.lower()]

            if not lines_list:
                if params.search_pattern:
                    return f"No matching entries found for pattern: '{params.search_pattern}'"
                return "Log file is empty or no lines to display"

            # Format output
            output = [
                f"# Log File: {params.file_path}",
                f"**Lines:** {len(lines_list)} (last {params.lines} requested)",
                "",
            ]

            if params.search_pattern:
                output.append(f"**Filtered by:** '{params.search_pattern}'")
                output.append("")

            output.append("```")
            output.extend([line.rstrip() for line in lines_list])
            output.append("```")

            result = "\n".join(output)
            return check_character_limit(result, "log file content")

        except Exception as e:
            return handle_error(e)
