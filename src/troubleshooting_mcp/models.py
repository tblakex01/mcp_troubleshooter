"""
Pydantic models for input validation across all tools.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .constants import ARGUMENT_BLOCKLIST, SAFE_COMMANDS


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
    def validate_args(self) -> "SafeCommandInput":
        command = self.command
        args = self.args or []

        if command in ARGUMENT_BLOCKLIST:
            blocked_args = ARGUMENT_BLOCKLIST[command]
            for arg in args:
                # Check exact match or prefix for flags (e.g., -f or -f...)
                # Also handle combined flags like -cf where -f is blocked
                if any(arg.startswith(blocked) for blocked in blocked_args):
                    raise ValueError(
                        f"Argument '{arg}' is not allowed for command '{command}'."
                    )
                # Check for combined short flags (if arg starts with - and not --)
                if arg.startswith("-") and not arg.startswith("--"):
                    for char in arg[1:]:
                        if f"-{char}" in blocked_args:
                            raise ValueError(
                                f"Flag '-{char}' (in '{arg}') is not allowed for command '{command}'."
                            )

        return self
