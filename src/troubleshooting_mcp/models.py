"""
Pydantic models for input validation across all tools.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .constants import SAFE_COMMANDS


class ResponseFormat(str, Enum):
    """Output format for tool responses."""

    MARKDOWN = "markdown"
    JSON = "json"


class SystemInfoInput(BaseModel):
    """Input model for system information queries."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )


class ResourceMonitorInput(BaseModel):
    """Input model for resource monitoring queries."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    include_per_cpu: bool | None = Field(
        default=False, description="Include per-CPU statistics (default: False)"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )


class LogFileInput(BaseModel):
    """Input model for log file operations."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    file_path: str | None = Field(
        default=None,
        description="Path to log file. If not provided, lists common log locations",
        max_length=500,
    )
    lines: int | None = Field(
        default=50,
        description="Number of lines to read from the end of the file (default: 50)",
        ge=1,
        le=1000,
    )
    search_pattern: str | None = Field(
        default=None, description="Optional grep pattern to filter log entries", max_length=200
    )


class NetworkDiagnosticInput(BaseModel):
    """Input model for network diagnostic operations."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra="forbid")

    host: str = Field(
        ...,
        description="Hostname or IP address to test (e.g., 'google.com', '8.8.8.8')",
        min_length=1,
        max_length=253,
    )
    port: int | None = Field(
        default=None,
        description="Port number to test connectivity (e.g., 80, 443, 22)",
        ge=1,
        le=65535,
    )
    timeout: int | None = Field(
        default=5,
        description="Timeout in seconds for the connection test (default: 5)",
        ge=1,
        le=30,
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Host cannot be empty or whitespace only")
        return v.strip()


class ProcessSearchInput(BaseModel):
    """Input model for process search operations."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    pattern: str | None = Field(
        default=None,
        description="Search pattern for process name (case-insensitive). If not provided, lists all processes",
        max_length=200,
    )
    limit: int | None = Field(
        default=20, description="Maximum number of processes to return (default: 20)", ge=1, le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )


class EnvironmentSearchInput(BaseModel):
    """Input model for environment variable operations."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    pattern: str | None = Field(
        default=None,
        description="Search pattern for environment variable names (case-insensitive)",
        max_length=200,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable",
    )


class SafeCommandInput(BaseModel):
    """Input model for safe command execution."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    command: str = Field(
        ...,
        description=f"Command to execute (must be one of: {', '.join(sorted(SAFE_COMMANDS))})",
        min_length=1,
        max_length=200,
    )
    args: list[str] | None = Field(
        default_factory=list,
        description="Command arguments (e.g., ['-a', '-l'] for 'ls -a -l')",
        max_items=20,
    )
    timeout: int | None = Field(
        default=30, description="Command timeout in seconds (default: 30)", ge=1, le=300
    )

    @field_validator("command")
    @classmethod
    def validate_command(cls, v: str) -> str:
        cmd = v.strip().lower()
        if cmd not in SAFE_COMMANDS:
            raise ValueError(
                f"Command '{v}' is not in the whitelist. "
                f"Allowed commands: {', '.join(sorted(SAFE_COMMANDS))}"
            )
        return cmd

    @model_validator(mode="after")
    def validate_safe_args(self) -> "SafeCommandInput":
        """Validate arguments for specific commands to prevent security risks."""
        command = self.command
        args = self.args or []

        # Convert args to lowercase for checking
        lower_args = [arg.lower() for arg in args]

        if command == "ip":
            # Prevent 'ip netns' (command injection) and destructive operations
            if "netns" in lower_args:
                raise ValueError("Argument 'netns' is not allowed for command 'ip'")

            # Check for other dangerous/destructive ip subcommands/args
            # 'link set' can modify interfaces
            # 'addr add/del/flush' can modify addresses
            # 'route add/del' can modify routing

            # Simple keyword blocking for destructive intents
            # 'exec' is used with netns, but also potentially other contexts
            if "exec" in lower_args:
                raise ValueError("Argument 'exec' is not allowed for command 'ip'")

            # 'link' is allowed (for show), but 'set' makes it destructive
            if "link" in lower_args and "set" in lower_args:
                raise ValueError("Operation 'link set' is not allowed for command 'ip'")

            # 'addr' is allowed (for show), but 'add', 'del', 'flush' are destructive
            # 'delete' is alias for 'del'
            destructive_actions = {"add", "del", "delete", "flush", "replace", "change"}
            if "addr" in lower_args or "address" in lower_args or "a" in lower_args:
                if any(action in lower_args for action in destructive_actions):
                    raise ValueError("Destructive address operations are not allowed")

        elif command == "ifconfig":
            # 'down' and 'up' are destructive/state-changing
            if "down" in lower_args or "up" in lower_args:
                raise ValueError("State changing arguments 'up'/'down' are not allowed for ifconfig")

        return self
