# Migration Guide - Troubleshooting MCP Server v1.0

This guide helps you understand the changes from the monolithic single-file structure to the new modular package structure.

## What Changed?

### Before (Single File)
```
troubleshooting_mcp/
├── troubleshooting_mcp.py    # 1,120 lines - everything in one file
├── test_server.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── EXAMPLES.md
├── CHANGELOG.md
├── LICENSE
└── claude_desktop_config.example.json
```

### After (Modular Package)
```
troubleshooting_mcp/
├── src/
│   └── troubleshooting_mcp/          # Main package
│       ├── __init__.py
│       ├── server.py                 # Entry point (24 lines)
│       ├── constants.py              # Configuration (38 lines)
│       ├── models.py                 # Input validation (177 lines)
│       ├── utils.py                  # Utilities (73 lines)
│       └── tools/                    # Individual tools
│           ├── __init__.py
│           ├── system_info.py        # ~165 lines
│           ├── resource_monitor.py   # ~155 lines
│           ├── log_reader.py         # ~165 lines
│           ├── network_diagnostic.py # ~120 lines
│           ├── process_search.py     # ~145 lines
│           ├── environment_inspect.py # ~140 lines
│           └── safe_command.py       # ~115 lines
│
├── tests/                            # Test directory
│   ├── __init__.py
│   └── test_server.py
│
├── docs/                             # Documentation
│   ├── QUICKSTART.md
│   ├── EXAMPLES.md
│   ├── CHANGELOG.md
│   └── ARCHITECTURE.md               # NEW
│
├── config/                           # Configuration
│   └── claude_desktop_config.example.json
│
├── troubleshooting_mcp.py            # Backward compatibility wrapper
├── setup.py                          # Package setup - NEW
├── pyproject.toml                    # Modern Python config - NEW
├── MANIFEST.in                       # Package manifest - NEW
├── .gitignore                        # Git ignore rules - NEW
├── MIGRATION_GUIDE.md                # This file - NEW
├── requirements.txt
├── LICENSE
└── README.md                         # Completely rewritten
```

## Breaking Changes

### ✅ None!

The new structure is **100% backward compatible**. Your existing Claude Desktop configuration will continue to work without any changes.

## Benefits of New Structure

### 1. **Modularity**
- Each tool in its own file (~100-165 lines each)
- Easy to find and modify specific functionality
- Clear separation of concerns

### 2. **Maintainability**
- Shared utilities in one place
- Constants centralized
- Input validation models grouped
- Easier to test individual components

### 3. **Extensibility**
- Add new tools by creating a new file
- No need to modify large monolithic file
- Clear pattern to follow

### 4. **Professional Structure**
- Follows Python packaging best practices
- Installable via pip
- Proper package structure for PyPI
- Can be imported as a library

### 5. **Better Documentation**
- Organized in docs/ folder
- Architecture documentation added
- Migration guide (this file)
- Clear project structure

## Migration Options

### Option 1: Keep Using Old Path (Recommended for Existing Users)

**No changes needed!** The root `troubleshooting_mcp.py` file still exists and works exactly as before.

Your existing config:
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

Continues to work without any modifications.

### Option 2: Install as Package (Recommended for New Users)

1. **Install the package:**
   ```bash
   cd /path/to/troubleshooting_mcp
   pip install -e .
   ```

2. **Update Claude Desktop config:**
   ```json
   {
     "mcpServers": {
       "troubleshooting": {
         "command": "troubleshooting-mcp"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

### Option 3: Use Module Syntax

1. **Update Claude Desktop config:**
   ```json
   {
     "mcpServers": {
       "troubleshooting": {
         "command": "python",
         "args": ["-m", "troubleshooting_mcp.server"],
         "cwd": "/absolute/path/to/troubleshooting_mcp"
       }
     }
   }
   ```

2. **Restart Claude Desktop**

## Code Changes

### How to Find Things

| Old Location | New Location |
|-------------|--------------|
| `CHARACTER_LIMIT` | `src/troubleshooting_mcp/constants.py` |
| `SAFE_COMMANDS` | `src/troubleshooting_mcp/constants.py` |
| `COMMON_LOG_PATHS` | `src/troubleshooting_mcp/constants.py` |
| `ResponseFormat` enum | `src/troubleshooting_mcp/models.py` |
| Input models (SystemInfoInput, etc.) | `src/troubleshooting_mcp/models.py` |
| `_format_bytes()` | `src/troubleshooting_mcp/utils.py` → `format_bytes()` |
| `_format_timestamp()` | `src/troubleshooting_mcp/utils.py` → `format_timestamp()` |
| `_handle_error()` | `src/troubleshooting_mcp/utils.py` → `handle_error()` |
| `_check_character_limit()` | `src/troubleshooting_mcp/utils.py` → `check_character_limit()` |
| `troubleshooting_get_system_info()` | `src/troubleshooting_mcp/tools/system_info.py` |
| `troubleshooting_monitor_resources()` | `src/troubleshooting_mcp/tools/resource_monitor.py` |
| `troubleshooting_read_log_file()` | `src/troubleshooting_mcp/tools/log_reader.py` |
| `troubleshooting_test_network_connectivity()` | `src/troubleshooting_mcp/tools/network_diagnostic.py` |
| `troubleshooting_search_processes()` | `src/troubleshooting_mcp/tools/process_search.py` |
| `troubleshooting_inspect_environment()` | `src/troubleshooting_mcp/tools/environment_inspect.py` |
| `troubleshooting_execute_safe_command()` | `src/troubleshooting_mcp/tools/safe_command.py` |

### Importing Components

```python
# Old way (still works with backward compat file)
import troubleshooting_mcp

# New way (package structure)
from troubleshooting_mcp import mcp
from troubleshooting_mcp.models import SystemInfoInput
from troubleshooting_mcp.utils import format_bytes
from troubleshooting_mcp.constants import SAFE_COMMANDS
```

## Customization

### Before: Edit Single File
1. Open `troubleshooting_mcp.py`
2. Find the section you want to modify
3. Make changes
4. Save

### After: Edit Specific Module
1. Navigate to relevant file:
   - Constants: `src/troubleshooting_mcp/constants.py`
   - Specific tool: `src/troubleshooting_mcp/tools/<tool_name>.py`
   - Utilities: `src/troubleshooting_mcp/utils.py`
2. Make changes
3. Save

**Example - Adding a log path:**

Before:
```python
# Line ~45 in troubleshooting_mcp.py
COMMON_LOG_PATHS = [
    "/var/log/syslog",
    # ... add here
]
```

After:
```python
# src/troubleshooting_mcp/constants.py
COMMON_LOG_PATHS = [
    "/var/log/syslog",
    "/custom/app.log",  # Add your path
]
```

## Testing the Migration

### 1. Verify Structure
```bash
cd /path/to/troubleshooting_mcp
python -c "from src.troubleshooting_mcp import mcp; print('✓ Import successful')"
```

### 2. Run Tests
```bash
python tests/test_server.py
```

### 3. Test Backward Compatibility
```bash
python troubleshooting_mcp.py --help
```

### 4. Test Package Installation
```bash
pip install -e .
troubleshooting-mcp --help
```

### 5. Test in Claude Desktop
- Restart Claude Desktop
- Ask: "What are the system specifications?"
- Verify tools are accessible

## Rollback Plan

If you encounter any issues:

### Quick Rollback
The old structure is preserved in git history. To rollback:

```bash
git log --oneline  # Find commit before migration
git checkout <commit-hash>
```

### Manual Rollback
1. The old monolithic file can be reconstructed by combining:
   - `src/troubleshooting_mcp/constants.py`
   - `src/troubleshooting_mcp/models.py`
   - `src/troubleshooting_mcp/utils.py`
   - All files in `src/troubleshooting_mcp/tools/`
   - `src/troubleshooting_mcp/server.py`

2. Or simply use the backward compatibility wrapper (it works identically)

## FAQ

### Q: Do I need to change my Claude Desktop config?
**A:** No! The existing configuration continues to work.

### Q: Will my existing scripts break?
**A:** No! The old entry point (`troubleshooting_mcp.py`) still exists and works the same way.

### Q: Can I still modify the code?
**A:** Yes! It's now easier since functionality is organized into smaller files.

### Q: What if I don't want to use the package structure?
**A:** You can continue using `troubleshooting_mcp.py` directly. The package structure is optional.

### Q: Is performance affected?
**A:** No. Import overhead is negligible (<0.1s). Runtime performance is identical.

### Q: Can I revert to the old structure?
**A:** Yes, though not recommended. The old file exists in git history or can be reconstructed.

### Q: Why was this change made?
**A:** To follow Python best practices, improve maintainability, and make the codebase easier to extend and contribute to.

## Getting Help

If you encounter issues during migration:

1. **Check the logs:**
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

2. **Verify Python path:**
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

3. **Test imports:**
   ```bash
   python -c "from src.troubleshooting_mcp import mcp; print('OK')"
   ```

4. **Check dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **Review documentation:**
   - README.md - Overview and setup
   - docs/QUICKSTART.md - Quick start guide
   - docs/ARCHITECTURE.md - Technical details
   - docs/EXAMPLES.md - Usage examples

## Summary

✅ **Backward compatible** - Old configuration still works
✅ **Better organized** - Each tool in its own file
✅ **Easier to maintain** - Clear module structure
✅ **More professional** - Follows Python best practices
✅ **Installable package** - Can use pip install
✅ **No breaking changes** - Everything still works

The migration provides significant benefits without requiring any immediate action from users.

