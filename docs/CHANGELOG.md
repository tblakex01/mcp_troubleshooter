# Changelog

All notable changes to the Troubleshooting MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-05

### Added
- Initial release of Troubleshooting MCP Server
- **System Information Tool**: Get comprehensive OS, hardware, and software details
  - Operating system and version information
  - CPU architecture and core counts
  - Memory and disk capacity
  - Python environment details
  - Support for both JSON and Markdown output formats

- **Resource Monitoring Tool**: Real-time system resource monitoring
  - Overall and per-core CPU usage
  - Memory (RAM) utilization with formatted byte sizes
  - Swap memory usage
  - Disk I/O statistics (read/write bytes and counts)
  - Network I/O statistics (sent/received bytes and packets)
  - Configurable per-CPU detail level

- **Log File Access Tool**: Read and analyze system logs
  - Tail-like functionality to read last N lines (1-1000)
  - Pattern-based filtering (grep-like functionality)
  - Common log location discovery for Linux and Windows
  - Support for large log files with efficient reading
  - Character limit protection with truncation

- **Network Diagnostics Tool**: Test network connectivity
  - DNS resolution testing with timing
  - TCP port connectivity checks
  - Configurable timeout (1-30 seconds)
  - Connection time measurements
  - Support for hostnames and IP addresses

- **Process Management Tool**: Search and monitor processes
  - Pattern-based process search (case-insensitive)
  - Process details including PID, name, CPU/memory usage
  - Process status and command line information
  - Sorted by CPU usage
  - Configurable result limits (1-100 processes)

- **Environment Analysis Tool**: Inspect system environment
  - Environment variable listing with pattern filtering
  - Development tool version detection (Python, Node, Git, Docker, etc.)
  - PATH configuration inspection
  - Support for both JSON and Markdown formats

- **Safe Command Execution Tool**: Execute whitelisted diagnostic commands
  - Strict command whitelist for security
  - Timeout protection (1-300 seconds)
  - Real-time stdout and stderr capture
  - Support for command arguments
  - Whitelisted commands: ping, traceroute, nslookup, dig, netstat, ss, ip, 
    ifconfig, df, du, free, uptime, uname, lsblk, lsof, whoami, hostname

### Security Features
- Input validation using Pydantic v2 models
- Command whitelist enforcement
- Timeout protection for all long-running operations
- Permission-aware error handling
- Character limit enforcement (25,000 characters)
- No privilege escalation

### Documentation
- Comprehensive README with installation and usage instructions
- Quick Start Guide for fast onboarding
- Example Claude Desktop configuration
- Tool-specific usage examples
- Security best practices
- Troubleshooting guide

### Technical Implementation
- Built with FastMCP (MCP Python SDK)
- Pydantic v2 for input validation
- psutil for system monitoring
- Async/await patterns throughout
- Comprehensive error handling
- Support for Linux, macOS, and Windows
- Python 3.10+ compatibility

### Tool Annotations
All tools properly annotated with:
- `readOnlyHint`: True (for read-only operations)
- `destructiveHint`: False (no destructive operations)
- `idempotentHint`: Appropriate for each tool
- `openWorldHint`: Appropriate for each tool

### Response Formats
- Markdown format (default): Human-readable with formatted output
- JSON format: Machine-readable structured data
- Consistent formatting across all tools
- Character limit protection with clear truncation messages

## [Unreleased]

### Planned Features
- Historical resource monitoring with time series data
- Log aggregation across multiple files
- Advanced network diagnostics (traceroute, mtr)
- System health scoring
- Alert threshold configuration
- Custom command whitelist configuration
- Log parsing and analysis tools
- Performance profiling tools
- Container and VM diagnostics
- Cloud provider integrations

### Under Consideration
- Real-time log streaming
- Automated diagnostic workflows
- Incident response playbooks
- Integration with monitoring systems
- Multi-host support
- Dashboard and visualization capabilities

---

## Version History

- **1.0.0** (2025-01-05): Initial release with core diagnostic tools

## Contributing

See [README.md](README.md) for contribution guidelines.

## Support

For issues and feature requests, please review the troubleshooting section in README.md.
