"""
Utility functions shared across the Troubleshooting MCP Server.
"""

from datetime import datetime

from .constants import CHARACTER_LIMIT


def format_bytes(bytes_value: int) -> str:
    """
    Convert bytes to human-readable format.

    Args:
        bytes_value: Number of bytes to format

    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_timestamp(timestamp: float) -> str:
    """
    Convert Unix timestamp to human-readable format.

    Args:
        timestamp: Unix timestamp (seconds since epoch)

    Returns:
        Formatted datetime string (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def handle_error(e: Exception) -> str:
    """
    Consistent error formatting across all tools.

    Args:
        e: Exception to format

    Returns:
        User-friendly error message
    """
    if isinstance(e, PermissionError):
        return (
            "Error: Permission denied. You may need elevated privileges to perform this operation."
        )
    elif isinstance(e, FileNotFoundError):
        return "Error: File or resource not found. Please check the path is correct."
    elif isinstance(e, TimeoutError):
        return "Error: Operation timed out. Please try again or increase the timeout value."
    elif isinstance(e, ValueError):
        return f"Error: Invalid input - {str(e)}"
    return f"Error: {type(e).__name__} - {str(e)}"


def check_character_limit(content: str, data_type: str = "response") -> str:
    """
    Check if response exceeds character limit and truncate if necessary.

    Args:
        content: Content to check
        data_type: Type of data being checked (for error message)

    Returns:
        Original content or truncated content with warning
    """
    if len(content) > CHARACTER_LIMIT:
        truncated = content[:CHARACTER_LIMIT]
        truncation_msg = (
            f"\n\n--- TRUNCATED ---\n"
            f"Response exceeded {CHARACTER_LIMIT} characters. "
            f"Original size: {len(content)} characters. "
            f"Consider using filters or limiting the scope of your query."
        )
        return truncated + truncation_msg
    return content
