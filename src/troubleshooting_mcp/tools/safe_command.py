"""
Safe Command Execution Tool - Execute whitelisted diagnostic commands.
"""

import shutil
import subprocess

from ..models import SafeCommandInput
from ..utils import check_character_limit, handle_error


def validate_safe_args(command: str, args: list[str]) -> str | None:
    """Validate arguments for specific commands to prevent security risks.

    Args:
        command: The command being executed
        args: List of arguments

    Returns:
        Error message if validation fails, None if safe
    """
    if not args:
        return None

    cmd = command.lower()

    if cmd == "ip":
        # Block network modification subcommands
        # ip link set, ip addr add, ip route del, etc.
        dangerous_keywords = {
            "set",
            "add",
            "del",
            "delete",
            "change",
            "replace",
            "flush",
            "exec",
            "tap",
            "tun",
            "netns",
        }
        for arg in args:
            if arg.lower() in dangerous_keywords:
                return f"Error: Security violation. Argument '{arg}' is not allowed for 'ip' command."

    elif cmd == "ifconfig":
        # Block modification keywords
        dangerous_keywords = {
            "up",
            "down",
            "add",
            "del",
            "metric",
            "mtu",
            "netmask",
            "broadcast",
            "pointopoint",
            "arp",
            "promisc",
        }
        for arg in args:
            if arg.lower() in dangerous_keywords:
                return f"Error: Security violation. Argument '{arg}' is not allowed for 'ifconfig' command."

    elif cmd == "hostname":
        # hostname with args usually sets the hostname unless it's a flag
        for arg in args:
            if not arg.startswith("-"):
                return "Error: Security violation. Setting hostname is not allowed."

    return None


def register_safe_command(mcp):
    """Register the safe command execution tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_execute_safe_command",
        annotations={
            "title": "Execute Safe Diagnostic Command",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_execute_safe_command(params: SafeCommandInput) -> str:
        """Execute whitelisted diagnostic commands safely with timeout protection.

        This tool executes a limited set of safe diagnostic commands that are commonly
        used for system troubleshooting. Only commands in the whitelist can be executed,
        and all commands run with a configurable timeout for safety.

        WHITELIST: ping, traceroute, nslookup, dig, netstat, ss, ip, ifconfig, df, du,
                   free, uptime, uname, lsblk, lsof, whoami, hostname

        Args:
            params (SafeCommandInput): Validated input parameters containing:
                - command (str): Command to execute (must be whitelisted)
                - args (Optional[List[str]]): Command arguments (max 20)
                - timeout (Optional[int]): Timeout in seconds (default: 30, max: 300)

        Returns:
            str: Command output or error message

            Success response: Command stdout and stderr output
            Error response: Timeout, permission denied, or command not found errors

        Examples:
            - Use when: "Ping google.com to check connectivity"
            - Use when: "Run df -h to check disk space"
            - Use when: "Execute uptime to see system uptime"
            - Don't use when: Command is not in the whitelist
            - Don't use when: You need to run potentially destructive operations

        Error Handling:
            - Returns "Error: Command not in whitelist" for unauthorized commands
            - Returns "Error: Command timed out" if execution exceeds timeout
            - Returns "Error: Permission denied" for commands requiring elevated privileges
            - Returns command stderr output if command fails

        Security Notes:
            - Only whitelisted commands can be executed
            - All commands run with timeout protection
            - Commands run with current user permissions (not elevated)
        """
        try:
            # Check if command exists on system
            command_path = shutil.which(params.command)
            if not command_path:
                return f"Error: Command '{params.command}' not found on this system"

            # Security check: Validate arguments
            security_error = validate_safe_args(params.command, params.args)
            if security_error:
                return security_error

            # Prepare command with arguments
            cmd_list = [command_path] + params.args

            # Execute command with timeout
            try:
                result = subprocess.run(
                    cmd_list, capture_output=True, text=True, timeout=params.timeout
                )

                output_lines = [
                    f"# Command Execution: {params.command}",
                    f"**Full Command:** `{' '.join(cmd_list)}`",
                    f"**Exit Code:** {result.returncode}",
                    "",
                ]

                if result.stdout:
                    output_lines.append("## Standard Output")
                    output_lines.append("```")
                    output_lines.append(result.stdout.strip())
                    output_lines.append("```")
                    output_lines.append("")

                if result.stderr:
                    output_lines.append("## Standard Error")
                    output_lines.append("```")
                    output_lines.append(result.stderr.strip())
                    output_lines.append("```")

                if not result.stdout and not result.stderr:
                    output_lines.append("*Command produced no output*")

                result_text = "\n".join(output_lines)
                return check_character_limit(result_text, "command output")

            except subprocess.TimeoutExpired:
                return (
                    f"Error: Command timed out after {params.timeout} seconds. "
                    f"Try increasing the timeout parameter or simplifying the command."
                )

        except Exception as e:
            return handle_error(e)
