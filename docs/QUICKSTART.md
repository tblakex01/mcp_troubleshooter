# Quick Start Guide - Troubleshooting MCP Server

Get up and running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
# Navigate to the server directory
cd /path/to/troubleshooting_mcp

# Install required packages
pip install -r requirements.txt
```

## Step 2: Test the Server (1 minute)

```bash
# Verify the server can start
python troubleshooting_mcp.py --help

# You should see MCP server initialization output
```

## Step 3: Configure Claude Desktop (2 minutes)

### macOS
1. Open: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the server configuration:

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

### Windows
1. Open: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the server configuration (use forward slashes or double backslashes):

```json
{
  "mcpServers": {
    "troubleshooting": {
      "command": "python",
      "args": ["C:/path/to/troubleshooting_mcp.py"]
    }
  }
}
```

## Step 4: Restart Claude Desktop (1 minute)

1. Completely quit Claude Desktop
2. Restart Claude Desktop
3. Look for the 🔌 icon indicating MCP servers are connected

## Step 5: Test It Out!

Try these example prompts in Claude:

**System Information:**
```
"What operating system and hardware specs does this system have?"
```

**Resource Monitoring:**
```
"Show me current CPU and memory usage"
```

**Check Logs:**
```
"What log files are available on this system?"
```

**Network Test:**
```
"Test connectivity to google.com on port 443"
```

**Process Search:**
```
"Are there any Python processes running?"
```

**Environment Check:**
```
"What development tools are installed and what are their versions?"
```

**Safe Command:**
```
"Run 'df -h' to check disk space"
```

## Troubleshooting Quick Fixes

### Server Not Appearing in Claude Desktop

1. **Check file path is absolute:**
   ```bash
   # Get absolute path
   python -c "import os; print(os.path.abspath('troubleshooting_mcp.py'))"
   ```

2. **Verify JSON syntax:**
   - Use a JSON validator
   - Check for trailing commas
   - Ensure proper quotes

3. **Check Claude Desktop logs:**
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### "Command not found" Error

```bash
# Check Python is in PATH
which python  # macOS/Linux
where python  # Windows

# Or use full path to Python in config:
# "command": "/usr/bin/python3"  # macOS/Linux
# "command": "C:/Python310/python.exe"  # Windows
```

### "Module not found" Error

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or use a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review tool-specific examples for advanced usage
- Customize `COMMON_LOG_PATHS` for your environment
- Explore combining multiple tools for comprehensive diagnostics

## Quick Reference Card

| What You Want | Tool to Use | Example Prompt |
|---------------|-------------|----------------|
| System specs | `get_system_info` | "What are the system specs?" |
| CPU/Memory usage | `monitor_resources` | "Show resource usage" |
| Read logs | `read_log_file` | "Show last 100 lines of syslog" |
| Test connectivity | `test_network_connectivity` | "Can I reach example.com?" |
| Find processes | `search_processes` | "Is nginx running?" |
| Check env vars | `inspect_environment` | "Show PATH variables" |
| Run command | `execute_safe_command` | "Run uptime command" |

---

**Need Help?** Review the full documentation in README.md or check the troubleshooting section.

**Ready to Customize?** See the Development section in README.md for extending the server.
