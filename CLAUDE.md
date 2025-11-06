# CLAUDE.md - Codebase Analysis

## Project Overview

**Name:** Troubleshooting MCP Server
**Version:** 1.0.0
**License:** MIT
**Python Requirement:** 3.10+

This is a Model Context Protocol (MCP) server that provides system troubleshooting and diagnostic tools for developers and system administrators. It enables LLMs like Claude to diagnose system issues, monitor resources, and test connectivity through a secure, well-structured interface.

---

## Project Purpose

The Troubleshooting MCP Server acts as a bridge between Claude Desktop and the operating system, providing diagnostic capabilities including:

- **System Information Retrieval** - OS details, hardware specs, CPU architecture, memory, Python version
- **Resource Monitoring** - Real-time CPU, memory, disk I/O, and network I/O metrics
- **Log File Analysis** - Read and filter system logs with grep-like pattern matching
- **Network Diagnostics** - DNS resolution and TCP port connectivity testing
- **Process Management** - Search and monitor running processes with resource usage
- **Environment Inspection** - Check environment variables and development tool versions
- **Safe Command Execution** - Execute whitelisted diagnostic commands with timeout protection

---

## Architecture

### High-Level Architecture

```
Claude Desktop (MCP Client)
        ↓ MCP Protocol
    FastMCP Server (server.py)
        ↓
Tool Registration Layer (tools/__init__.py)
        ↓
Individual Tool Modules (7 diagnostic tools)
        ↓
Shared Components (models, utils, constants)
        ↓
System Libraries (psutil, socket, subprocess, os)
        ↓
Operating System
```

### Directory Structure

```
/home/user/mcp_troubleshooter/
├── src/troubleshooting_mcp/          # Main package
│   ├── __init__.py                   # Package initialization
│   ├── server.py                     # FastMCP server entry point
│   ├── constants.py                  # Configuration constants
│   ├── models.py                     # Pydantic input validation models
│   ├── utils.py                      # Shared utility functions
│   └── tools/                        # 7 diagnostic tools
│       ├── __init__.py               # Tool registration orchestrator
│       ├── system_info.py            # System information retrieval
│       ├── resource_monitor.py       # Real-time resource monitoring
│       ├── log_reader.py             # Log file reader with filtering
│       ├── network_diagnostic.py     # Network connectivity testing
│       ├── process_search.py         # Process monitoring and search
│       ├── environment_inspect.py    # Environment variables & tools
│       └── safe_command.py           # Whitelisted command execution
├── tests/                            # Test suite
├── docs/                             # Comprehensive documentation
├── config/                           # Configuration examples
├── troubleshooting_mcp.py            # Backward compatibility wrapper
├── README.md                         # Main documentation
├── pyproject.toml                    # Modern Python project config
└── setup.py                          # Package setup script
```

---

## Core Components

### Entry Point: `server.py`

Located at: `src/troubleshooting_mcp/server.py`

This is the main entry point that:
- Creates the FastMCP server instance
- Registers all 7 diagnostic tools
- Configures server metadata
- Provides the `main()` function for execution

**Running the server:**
```bash
# Method 1: Direct execution
python troubleshooting_mcp.py

# Method 2: Module execution
python -m troubleshooting_mcp.server

# Method 3: After installation
troubleshooting-mcp
```

### Configuration: `constants.py`

Located at: `src/troubleshooting_mcp/constants.py`

Key configurations:
- **CHARACTER_LIMIT = 25000** - Maximum response size to prevent output explosion
- **SAFE_COMMANDS** - Whitelist of 17 allowed diagnostic commands
- **COMMON_LOG_PATHS** - Default system log file locations

### Input Validation: `models.py`

Located at: `src/troubleshooting_mcp/models.py`

Uses Pydantic v2 for robust input validation with 7 models:

1. **SystemInfoInput** - response_format only
2. **ResourceMonitorInput** - CPU monitoring options
3. **LogFileInput** - File path, lines (1-1000), search pattern
4. **NetworkDiagnosticInput** - Host (required), port, timeout (1-30s)
5. **ProcessSearchInput** - Pattern, limit (1-100), format
6. **EnvironmentSearchInput** - Pattern, format
7. **SafeCommandInput** - Command validation, args (max 20), timeout

### Utilities: `utils.py`

Located at: `src/troubleshooting_mcp/utils.py`

Shared helper functions:
- `format_bytes()` - Human-readable byte formatting (B, KB, MB, GB, TB)
- `format_timestamp()` - Unix timestamp to readable date/time
- `handle_error()` - Consistent error formatting with specific exception handling
- `check_character_limit()` - Enforces output size limits with truncation warnings

---

## The 7 Diagnostic Tools

### 1. System Info (`system_info.py`)
**MCP Name:** `troubleshooting_get_system_info`
**Purpose:** Get OS details, CPU architecture, memory, disk, and Python version
**Location:** `src/troubleshooting_mcp/tools/system_info.py:17`

### 2. Resource Monitor (`resource_monitor.py`)
**MCP Name:** `troubleshooting_monitor_resources`
**Purpose:** Real-time monitoring of CPU, memory, disk I/O, and network I/O
**Location:** `src/troubleshooting_mcp/tools/resource_monitor.py:17`

### 3. Log Reader (`log_reader.py`)
**MCP Name:** `troubleshooting_read_log_file`
**Purpose:** Read and filter system log files with pattern matching
**Location:** `src/troubleshooting_mcp/tools/log_reader.py:16`

### 4. Network Diagnostic (`network_diagnostic.py`)
**MCP Name:** `troubleshooting_test_network_connectivity`
**Purpose:** Test DNS resolution and TCP port connectivity
**Location:** `src/troubleshooting_mcp/tools/network_diagnostic.py:17`

### 5. Process Search (`process_search.py`)
**MCP Name:** `troubleshooting_search_processes`
**Purpose:** Search and monitor running processes with resource usage
**Location:** `src/troubleshooting_mcp/tools/process_search.py:17`

### 6. Environment Inspector (`environment_inspect.py`)
**MCP Name:** `troubleshooting_inspect_environment`
**Purpose:** Check environment variables and development tool versions
**Location:** `src/troubleshooting_mcp/tools/environment_inspect.py:17`

### 7. Safe Command Executor (`safe_command.py`)
**MCP Name:** `troubleshooting_execute_safe_command`
**Purpose:** Execute whitelisted diagnostic commands with timeout protection
**Location:** `src/troubleshooting_mcp/tools/safe_command.py:17`

**Tool Characteristics:**
- All tools are async functions
- Support both Markdown and JSON output formats
- Include comprehensive docstrings with examples
- Have `readOnlyHint: True` annotation (no system modifications)
- Proper error handling with descriptive messages

---

## Security Architecture

### Multi-Layer Security

1. **Command Whitelisting**
   - Only 17 predefined commands allowed
   - Commands: ping, traceroute, nslookup, dig, netstat, ss, ip, ifconfig, df, du, free, uptime, uname, lsblk, lsof, whoami, hostname
   - No arbitrary command execution

2. **Input Validation**
   - Pydantic models enforce type checking
   - Range constraints (e.g., lines: 1-1000, timeout: 1-30s)
   - Pattern validation for hostnames and commands
   - Automatic whitespace stripping

3. **Timeout Protection**
   - All operations have configurable timeouts
   - Default: 30 seconds for commands, 5 seconds for network tests
   - Prevents hanging operations

4. **Permission Handling**
   - No privilege escalation
   - Clear error messages for permission denied
   - Read-only operations only

5. **Output Limits**
   - CHARACTER_LIMIT = 25000 characters
   - Automatic truncation with warnings
   - Prevents memory exhaustion

---

## Design Patterns

### 1. Modular Architecture
- Each diagnostic tool is isolated in its own module
- Clear separation of concerns
- Easy to extend without modifying existing code

### 2. Factory Pattern
- `register_all_tools()` function acts as a factory
- Each tool has its own `register_*()` function
- Centralized tool registration

### 3. Input Validation Pattern
- All inputs validated using Pydantic models
- Type safety enforced at the model level
- Custom validators for domain-specific constraints

### 4. Command Pattern
- Each tool is registered as an async callable
- Tools decorated with `@mcp.tool()` with metadata
- Consistent interface across all tools

### 5. Utility/Helper Pattern
- Shared formatting functions
- Centralized error handling
- Reusable character limit enforcement

---

## Key Dependencies

### Core Dependencies
1. **mcp >= 1.0.0** - Model Context Protocol Python SDK with FastMCP framework
2. **psutil >= 5.9.0** - Cross-platform system and process monitoring library
3. **pydantic >= 2.0.0** - Data validation using Python type annotations

### Development Dependencies
- pytest >= 8.0.0 (testing framework)
- pytest-asyncio >= 0.21.0 (async test support)
- pytest-cov >= 4.0.0 (coverage reporting)
- black >= 25.0.0 (code formatting)
- ruff >= 0.14.0 (linting and import sorting)
- mypy >= 1.0.0 (static type checking)

### Standard Library Usage
- `socket` - Network connectivity testing
- `subprocess` - Safe command execution
- `os/sys` - Environment and system information
- `json` - Output formatting
- `pathlib` - File path handling

---

## Configuration Files

### `pyproject.toml`
Modern Python project configuration including:
- Project metadata (name, version, author, license)
- Dependency specifications (core and dev)
- Tool configurations for Black, Ruff, MyPy, Pytest

**Key Settings:**
- Black: line-length 100, Python 3.10+
- Ruff: linting rules (E, W, F, I, B, C4, UP)
- Pytest: async mode auto, coverage reporting

### `setup.py`
Backward-compatible package installation:
- Entry point: `troubleshooting-mcp`
- Package discovery from `src/` directory
- Setuptools configuration

### `pytest.ini`
Testing configuration:
- Test discovery patterns
- Coverage reports (term, HTML, XML)
- Custom markers (unit, integration, slow)

### `claude_desktop_config.example.json`
MCP client configuration template for Claude Desktop

---

## Code Quality Standards

### Style and Formatting
- **PEP 8 compliant** - Standard Python style guide
- **Type hints throughout** - Full type annotation coverage
- **Comprehensive docstrings** - All functions documented with examples
- **100 character line length** - Configured in Black

### Quality Tools
- **Black** - Automatic code formatting
- **Ruff** - Fast linting and import sorting
- **MyPy** - Static type checking
- **Coverage** - Test coverage tracking

### Version Control
- Comprehensive `.gitignore` covering Python, IDEs, OS files, and secrets
- Git repository initialized with structured commits

---

## Testing Framework

**Test File:** `tests/test_server.py`

**Test Coverage:**
- Python version verification (3.10+)
- Dependency checking (mcp, psutil, pydantic)
- Server imports validation
- psutil functionality tests
- Pydantic model validation
- Overall server status

**Running Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=troubleshooting_mcp

# Run specific test markers
pytest -m unit
pytest -m integration
```

---

## Documentation

### Available Documentation

1. **README.md** - Comprehensive main documentation (500+ lines)
   - Features overview, installation, configuration, security, troubleshooting

2. **docs/QUICKSTART.md** - 5-minute setup guide
   - Quick start for getting the server running

3. **docs/EXAMPLES.md** - Detailed usage examples for each tool
   - Practical examples of all 7 diagnostic tools

4. **docs/CHANGELOG.md** - Version history and changes
   - Track changes across versions

5. **docs/ARCHITECTURE.md** - Technical architecture documentation
   - Architecture diagram, component structure, data flow

6. **docs/FOLDER_STRUCTURE.md** - Directory organization guide
   - Detailed explanation of project structure

7. **PROJECT_SUMMARY.md** - Project overview and statistics
   - High-level project information

8. **MIGRATION_GUIDE.md** - Migration documentation
   - Guide for refactoring and updates

---

## Development Workflow

### Installation for Development
```bash
# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Quality Checks
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest --cov=troubleshooting_mcp --cov-report=html
```

### Adding a New Tool

1. Create a new file in `src/troubleshooting_mcp/tools/`
2. Define input model in `models.py`
3. Implement the tool function with `@mcp.tool()` decorator
4. Create a `register_*()` function
5. Add registration call to `tools/__init__.py:register_all_tools()`
6. Update documentation

---

## Platform Support

**Supported Operating Systems:**
- Linux (primary development platform)
- macOS (cross-platform via psutil)
- Windows (cross-platform via psutil)

**Supported Python Versions:**
- Python 3.10
- Python 3.11
- Python 3.12

---

## Key Architectural Insights

### Strengths
1. **Clean modular architecture** - Clear separation of concerns
2. **Comprehensive security** - Whitelisting, validation, timeouts
3. **Well-documented** - Detailed docstrings and comprehensive docs
4. **Flexible output** - Both Markdown and JSON formats
5. **Cross-platform** - Works on Linux, macOS, Windows
6. **Proper error handling** - Descriptive error messages throughout
7. **Async/await support** - Handles long-running operations
8. **Extensible design** - Easy to add new tools

### Design Decisions
1. **Pydantic for validation** - Robust input validation with type safety
2. **FastMCP framework** - Simplified MCP server implementation
3. **psutil library** - Cross-platform system monitoring
4. **Modular tools** - Each tool is independent and focused
5. **Character limits** - Prevents output explosion
6. **Whitelisting approach** - Security-first design for command execution

### Scalability Considerations
1. Each tool is independent and can be modified without affecting others
2. New tools can be added by creating a module and registering it
3. Shared utilities reduce code duplication
4. Configurable constants allow customization without code changes

---

## Common Operations

### Starting the Server
```bash
# Development mode
python troubleshooting_mcp.py

# Production mode (after installation)
troubleshooting-mcp
```

### Integration with Claude Desktop
Add to Claude Desktop configuration:
```json
{
  "mcpServers": {
    "troubleshooting": {
      "command": "python",
      "args": ["/path/to/troubleshooting_mcp.py"]
    }
  }
}
```

### Example Tool Usage (via Claude)
Once configured, Claude can invoke tools like:
- "What are the system specs?"
- "Monitor CPU and memory usage"
- "Check if port 8080 is accessible on localhost"
- "Search for python processes"
- "Read the last 50 lines of the system log"

---

## Project Status

**Current Version:** 1.0.0
**Status:** Beta (Development Status :: 4)
**Last Updated:** 2025-01-05
**Target Audience:** Developers, System Administrators

---

## Additional Resources

- **Project Repository:** Local Git repository initialized
- **Issue Tracking:** See documentation for troubleshooting
- **Contributing:** Follow code quality standards and testing requirements
- **License:** MIT License - see LICENSE file

---

## Summary

This is a production-ready MCP server with:
- ✅ Clean architecture and modular design
- ✅ Comprehensive security measures
- ✅ Extensive documentation
- ✅ Full test coverage setup
- ✅ Cross-platform compatibility
- ✅ Professional code quality standards
- ✅ Easy extensibility for new tools

The codebase follows Python best practices and provides a solid foundation for system diagnostics through Claude Desktop.
