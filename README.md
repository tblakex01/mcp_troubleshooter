# Troubleshooting MCP Server

A Model Context Protocol (MCP) server that provides comprehensive system troubleshooting and diagnostic tools for developers and system administrators. This server enables LLMs to help diagnose system issues, monitor resources, check logs, test connectivity, and more.

**Version:** 1.0.0 | **License:** MIT | **Python:** 3.10+

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation Methods](#installation-methods)
- [Available Tools](#available-tools)
- [Configuration](#configuration)
- [Security](#security)
- [Development](#development)
- [Documentation](#documentation)

---

## ✨ Features

### 🖥️ System Information
Get comprehensive details about the operating system, hardware specifications, CPU architecture, memory capacity, and installed software versions.

### 📊 Resource Monitoring
Real-time monitoring of system resources including:
- CPU usage (overall and per-core)
- Memory utilization (RAM and swap)
- Disk I/O statistics
- Network I/O metrics

### 📋 Log File Access
Read and analyze system log files with:
- Tail-like functionality to read last N lines
- Pattern-based filtering (similar to grep)
- Common log location discovery
- Support for various log formats

### 🌐 Network Diagnostics
Test network connectivity with:
- DNS resolution testing
- TCP port connectivity checks
- Connection timing measurements
- Timeout configuration

### ⚙️ Process Management
Search and monitor running processes:
- Pattern-based process search
- CPU and memory usage per process
- Process status and command line details
- Sorted by resource usage

### 🔧 Environment Analysis
Inspect system environment including:
- Environment variables (with pattern filtering)
- Installed development tools and versions
- PATH configuration
- Common tool version checks (git, docker, python, node, etc.)

### 🛡️ Safe Command Execution
Execute whitelisted diagnostic commands with:
- Strict command whitelist for security
- Timeout protection
- Safe diagnostic operations only
- Real-time output capture

---

## 📁 Project Structure

```
troubleshooting_mcp/
├── src/
│   └── troubleshooting_mcp/          # Main package
│       ├── __init__.py               # Package initialization
│       ├── server.py                 # MCP server entry point
│       ├── constants.py              # Shared constants
│       ├── models.py                 # Pydantic input validation models
│       ├── utils.py                  # Utility functions
│       └── tools/                    # Individual diagnostic tools
│           ├── __init__.py           # Tool registration
│           ├── system_info.py        # System information tool
│           ├── resource_monitor.py   # Resource monitoring tool
│           ├── log_reader.py         # Log file reader tool
│           ├── network_diagnostic.py # Network diagnostic tool
│           ├── process_search.py     # Process search tool
│           ├── environment_inspect.py # Environment inspection tool
│           └── safe_command.py       # Safe command execution tool
│
├── tests/                            # Test suite
│   ├── __init__.py
│   └── test_server.py                # Server validation tests
│
├── docs/                             # Documentation
│   ├── QUICKSTART.md                 # Quick start guide
│   ├── EXAMPLES.md                   # Detailed usage examples
│   └── CHANGELOG.md                  # Version history
│
├── config/                           # Configuration files
│   └── claude_desktop_config.example.json # Claude Desktop example config
│
├── troubleshooting_mcp.py            # Backward compatibility entry point
├── setup.py                          # Package setup script
├── pyproject.toml                    # Modern Python project configuration
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
└── README.md                         # This file
```

### 🎯 Key Design Principles

1. **Modular Architecture**: Each diagnostic tool is in its own module for easy maintenance and testing
2. **Clear Separation**: Constants, models, utilities, and tools are separated for clarity
3. **Backward Compatibility**: The root `troubleshooting_mcp.py` maintains compatibility with existing configurations
4. **Installable Package**: Can be installed with `pip install -e .` for system-wide access
5. **Type Safety**: Uses Pydantic v2 for comprehensive input validation
6. **Security First**: Strict whitelists, timeout protection, and input validation throughout

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies (1 minute)

```bash
# Navigate to the project directory
cd troubleshooting_mcp

# Install required packages
pip install -r requirements.txt

# Or install as a package (recommended)
pip install -e .
```

### 2️⃣ Test the Server (1 minute)

```bash
# Method 1: Run directly (backward compatible)
python troubleshooting_mcp.py --help

# Method 2: Run as module
python -m troubleshooting_mcp.server --help

# Method 3: If installed as package
troubleshooting-mcp --help

# Run validation tests
python tests/test_server.py
```

### 3️⃣ Configure Claude Desktop (2 minutes)

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "troubleshooting": {
      "command": "python",
      "args": ["/absolute/path/to/troubleshooting_mcp.py"]
    }
  }
}
```

**Alternative (if installed as package):**
```json
{
  "mcpServers": {
    "troubleshooting": {
      "command": "troubleshooting-mcp"
    }
  }
}
```

### 4️⃣ Restart Claude Desktop

1. Completely quit Claude Desktop
2. Restart Claude Desktop
3. Look for the 🔌 icon indicating MCP servers are connected

---

## 📦 Installation Methods

### Method 1: Direct Use (No Installation)
```bash
python troubleshooting_mcp.py
```
Pros: Simple, no installation needed
Cons: Not accessible system-wide

### Method 2: Editable Install (Development)
```bash
pip install -e .
troubleshooting-mcp
```
Pros: System-wide access, easy to modify, auto-updates
Cons: Requires pip install

### Method 3: Standard Install (Production)
```bash
pip install .
troubleshooting-mcp
```
Pros: Clean installation, system-wide access
Cons: Requires reinstall after changes

### Method 4: Module Execution
```bash
python -m troubleshooting_mcp.server
```
Pros: No installation, proper Python module syntax
Cons: Requires being in parent directory

---

## 🛠 Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `troubleshooting_get_system_info` | Get comprehensive system details | "What are the system specs?" |
| `troubleshooting_monitor_resources` | Monitor CPU, memory, disk, network | "Show current resource usage" |
| `troubleshooting_read_log_file` | Read and filter log files | "Show last 100 lines of syslog" |
| `troubleshooting_test_network_connectivity` | Test host/port connectivity | "Can I reach google.com?" |
| `troubleshooting_search_processes` | Search running processes | "Is nginx running?" |
| `troubleshooting_inspect_environment` | Check environment variables & tools | "What dev tools are installed?" |
| `troubleshooting_execute_safe_command` | Run whitelisted commands | "Run df -h to check disk space" |

For detailed tool documentation and examples, see [docs/EXAMPLES.md](docs/EXAMPLES.md).

---

## ⚙️ Configuration

### Dependencies
- `mcp>=1.0.0` - MCP Python SDK with FastMCP framework
- `psutil>=5.9.0` - System and process monitoring
- `pydantic>=2.0.0` - Input validation

### Environment Variables
The server respects standard Python environment variables:
- `PYTHONPATH` - For module resolution
- `PATH` - For locating diagnostic commands

### Customization

**Log Paths:** Edit `src/troubleshooting_mcp/constants.py`:
```python
COMMON_LOG_PATHS = [
    "/var/log/syslog",
    "/custom/app/logs/error.log",
    # Add your custom paths
]
```

**Safe Commands:** Edit `src/troubleshooting_mcp/constants.py`:
```python
SAFE_COMMANDS = {
    "ping", "traceroute", "netstat",
    # Add approved commands only
}
```

**Character Limit:** Edit `src/troubleshooting_mcp/constants.py`:
```python
CHARACTER_LIMIT = 25000  # Adjust as needed
```

---

## 🔒 Security

### Command Whitelist
Only pre-approved diagnostic commands can be executed. The whitelist includes common troubleshooting tools but excludes any commands that could:
- Modify system state
- Delete or overwrite files
- Change permissions
- Install software
- Execute arbitrary code

**Default Whitelist:** `ping`, `traceroute`, `nslookup`, `dig`, `netstat`, `ss`, `ip`, `ifconfig`, `df`, `du`, `free`, `uptime`, `uname`, `lsblk`, `lsof`, `whoami`, `hostname`

### Timeout Protection
All long-running operations have configurable timeouts:
- Command execution: 30 seconds default, 300 seconds maximum
- Network tests: 5 seconds default, 30 seconds maximum

### Permission Handling
- No privilege escalation
- Clear error messages for permission-denied scenarios
- Read-only operations where possible

### Input Validation
All inputs are validated using Pydantic models with:
- Type checking
- Range constraints
- Pattern validation
- Whitelist verification

---

## 💻 Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd troubleshooting_mcp

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .

# Run tests
python tests/test_server.py
```

### Adding New Tools

1. **Create new tool module** in `src/troubleshooting_mcp/tools/`:
```python
# src/troubleshooting_mcp/tools/my_tool.py
def register_my_tool(mcp):
    @mcp.tool(name="troubleshooting_my_tool", annotations={...})
    async def troubleshooting_my_tool(params: MyInput) -> str:
        # Implementation
        pass
```

2. **Add input model** in `src/troubleshooting_mcp/models.py`:
```python
class MyInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    param: str = Field(..., description="...")
```

3. **Register in tools package** `src/troubleshooting_mcp/tools/__init__.py`:
```python
from .my_tool import register_my_tool

def register_all_tools(mcp):
    # ... existing registrations ...
    register_my_tool(mcp)
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add comprehensive docstrings to all functions
- Keep tools modular and focused
- Use the shared utility functions

### Testing

```bash
# Run all tests
python tests/test_server.py

# Test specific functionality
python -c "from src.troubleshooting_mcp import mcp; print('Import successful')"
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - Overview and getting started |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | 5-minute quick start guide |
| [docs/EXAMPLES.md](docs/EXAMPLES.md) | Detailed usage examples for each tool |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Version history and changes |
| [config/claude_desktop_config.example.json](config/claude_desktop_config.example.json) | Example Claude Desktop configuration |

---

## 🎯 Example Usage

Once configured in Claude Desktop, try these prompts:

### System Diagnostics
```
"What operating system and hardware does this machine have?"
"Show me current CPU and memory usage"
```

### Log Analysis
```
"What log files are available on this system?"
"Search nginx error logs for 500 errors in the last 200 lines"
```

### Network Testing
```
"Can this server reach google.com?"
"Test if port 443 is open on api.example.com"
```

### Process Management
```
"Is docker running on this system?"
"Show me the top 10 processes by CPU usage"
```

### Environment Inspection
```
"What development tools are installed?"
"Show me all AWS-related environment variables"
```

---

## 🐛 Troubleshooting

### Server Not Appearing in Claude Desktop
1. Check file path is absolute in config
2. Verify JSON syntax (no trailing commas)
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### "Module not found" Error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### "Command not found" Error
```bash
# Check Python is in PATH
which python  # macOS/Linux
where python  # Windows

# Or use full path in config
# "command": "/usr/bin/python3"  # macOS/Linux
# "command": "C:/Python310/python.exe"  # Windows
```

---

## 🤝 Contributing

Contributions are welcome! When contributing:

1. Follow the existing code style and modular architecture
2. Add comprehensive docstrings and type hints
3. Include input validation using Pydantic
4. Implement proper error handling
5. Update documentation
6. Test on multiple platforms (Linux, macOS, Windows)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built using:
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) by Anthropic
- [FastMCP](https://github.com/modelcontextprotocol/python-sdk) - Python MCP SDK
- [psutil](https://github.com/giampaolo/psutil) - System monitoring library
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

## 📞 Support

For issues, questions, or suggestions:
- Review the troubleshooting section above
- Check the [QUICKSTART guide](docs/QUICKSTART.md)
- Review [EXAMPLES documentation](docs/EXAMPLES.md)
- Check the MCP documentation: https://modelcontextprotocol.io/

---

**Made with ❤️ for developers and system administrators**

*Last Updated: 2025-01-05 | Version: 1.0.0*
