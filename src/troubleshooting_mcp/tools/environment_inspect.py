"""
Environment Inspection Tool - Inspect environment variables and development tools.
"""

import json
import os
import shutil
import subprocess

from ..models import EnvironmentSearchInput, ResponseFormat
from ..utils import check_character_limit, handle_error

# Sensitive keywords for environment variable masking
# Variables containing these keywords (as whole words) will have their values masked
SENSITIVE_KEYWORDS = {
    "KEY",
    "SECRET",
    "PASSWORD",
    "TOKEN",
    "AUTH",
    "CREDENTIAL",
    "PRIVATE",
    "CERTIFICATE",
    "SIGNATURE",
}


def _is_sensitive_variable(var_name: str) -> bool:
    """Check if an environment variable name contains sensitive keywords.
    
    Uses word boundary matching to avoid false positives like KEYBOARD, MONKEY, DONKEY.
    A keyword matches if it appears as a complete word (separated by underscores or at boundaries).
    
    Args:
        var_name: The environment variable name to check
        
    Returns:
        True if the variable name contains sensitive keywords, False otherwise
        
    Examples:
        >>> _is_sensitive_variable("API_KEY")
        True
        >>> _is_sensitive_variable("MY_SECRET")
        True
        >>> _is_sensitive_variable("KEYBOARD")
        False
        >>> _is_sensitive_variable("MONKEY_ISLAND")
        False
    """
    # Split the variable name by underscores to get word components
    parts = var_name.upper().split("_")
    
    # Check if any part exactly matches a sensitive keyword
    return any(part in SENSITIVE_KEYWORDS for part in parts)


def register_environment_inspect(mcp):
    """Register the environment inspection tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_inspect_environment",
        annotations={
            "title": "Inspect Environment Variables",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    async def troubleshooting_inspect_environment(params: EnvironmentSearchInput) -> str:
        """Inspect environment variables and development tool versions.

        This tool retrieves environment variables with optional filtering by pattern,
        and also checks for common development tools (git, docker, python, node, etc.)
        and their versions. Useful for debugging environment-specific issues.

        Args:
            params (EnvironmentSearchInput): Validated input parameters containing:
                - pattern (Optional[str]): Search pattern for env var names (case-insensitive)
                - response_format (ResponseFormat): Output format ('markdown' or 'json')

        Returns:
            str: Environment information in the requested format

            Success response includes:
            - Filtered environment variables (if pattern provided)
            - Installed development tools and versions
            - System PATH components

        Examples:
            - Use when: "What environment variables are set?"
            - Use when: "Show me all PATH-related variables"
            - Use when: "What version of Docker is installed?"
            - Use when: "List all AWS-related environment variables"
            - Don't use when: You need to modify environment variables

        Error Handling:
            - Returns empty list if no variables match pattern
            - Handles tool version check failures gracefully
        """
        try:
            # Get environment variables
            env_vars = {}

            for key, value in os.environ.items():
                if params.pattern:
                    if params.pattern.lower() not in key.lower():
                        continue

                # Mask sensitive values using word boundary matching
                # This prevents false positives like KEYBOARD, MONKEY, DONKEY
                is_sensitive = _is_sensitive_variable(key)
                if is_sensitive:
                    env_vars[key] = "******** (masked for security)"
                else:
                    env_vars[key] = value

            # Check for common development tools
            dev_tools = {}
            tools_to_check = [
                ("python", ["--version"]),
                ("python3", ["--version"]),
                ("node", ["--version"]),
                ("npm", ["--version"]),
                ("git", ["--version"]),
                ("docker", ["--version"]),
                ("kubectl", ["version", "--client", "--short"]),
                ("terraform", ["--version"]),
                ("ansible", ["--version"]),
            ]

            for tool, args in tools_to_check:
                try:
                    if shutil.which(tool):
                        result = subprocess.run(
                            [tool] + args, capture_output=True, text=True, timeout=5
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                        dev_tools[tool] = version.split("\n")[0]
                except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
                    pass

            if params.response_format == ResponseFormat.MARKDOWN:
                lines = ["# Environment Analysis", ""]

                # Development tools section
                if dev_tools:
                    lines.append("## Installed Development Tools")
                    for tool, version in sorted(dev_tools.items()):
                        lines.append(f"- **{tool}:** {version}")
                    lines.append("")

                # Environment variables section
                lines.append("## Environment Variables")
                if params.pattern:
                    lines.append(f"**Filter:** '{params.pattern}'")
                lines.append(f"**Count:** {len(env_vars)}")
                lines.append("")

                if env_vars:
                    # Sort for consistent output
                    for key in sorted(env_vars.keys()):
                        value = env_vars[key]
                        # Truncate very long values
                        if len(value) > 200:
                            value = value[:200] + "... (truncated)"
                        lines.append(f"**{key}:**")
                        lines.append(f"```\n{value}\n```")
                        lines.append("")
                else:
                    lines.append("*No matching environment variables found*")

                result = "\n".join(lines)
                return check_character_limit(result, "environment data")
            else:
                data = {
                    "dev_tools": dev_tools,
                    "environment_variables": env_vars,
                    "filter": params.pattern,
                    "count": len(env_vars),
                }
                return json.dumps(data, indent=2)

        except Exception as e:
            return handle_error(e)
