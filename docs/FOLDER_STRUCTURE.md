# Troubleshooting MCP Server - Folder Structure Reference

This document provides a detailed reference of the project's folder structure with explanations for each component.

## 📁 Complete Structure

```
troubleshooting_mcp/
│
├── 📄 Root Files
│   ├── README.md                        Main documentation & getting started
│   ├── LICENSE                          MIT License
│   ├── requirements.txt                 Python dependencies (mcp, psutil, pydantic)
│   ├── setup.py                         Package installation script
│   ├── pyproject.toml                   Modern Python project configuration (PEP 518)
│   ├── MANIFEST.in                      Package manifest (what to include in dist)
│   ├── .gitignore                       Git ignore rules (Python standard)
│   ├── MIGRATION_GUIDE.md               Guide for migrating from old structure
│   ├── PROJECT_SUMMARY.md               Project overview and statistics
│   ├── REORGANIZATION_COMPLETE.md       Reorganization summary
│   └── troubleshooting_mcp.py           Backward compatibility entry point
│
├── 📁 src/                              Source code root
│   └── 📁 troubleshooting_mcp/          Main package
│       │
│       ├── 📄 __init__.py               Package initialization & exports
│       │                                - Exports: mcp server instance
│       │                                - Defines: __version__, __author__, __license__
│       │
│       ├── 📄 server.py                 MCP server entry point
│       │                                - Initializes FastMCP server
│       │                                - Registers all tools
│       │                                - Provides main() function
│       │
│       ├── 📄 constants.py              Configuration constants
│       │                                - CHARACTER_LIMIT (25,000)
│       │                                - SAFE_COMMANDS (whitelist)
│       │                                - COMMON_LOG_PATHS
│       │
│       ├── 📄 models.py                 Pydantic input validation models
│       │                                - ResponseFormat enum
│       │                                - 7 input models (one per tool)
│       │                                - Field validators
│       │
│       ├── 📄 utils.py                  Shared utility functions
│       │                                - format_bytes()
│       │                                - format_timestamp()
│       │                                - handle_error()
│       │                                - check_character_limit()
│       │
│       └── 📁 tools/                    Diagnostic tool modules
│           │
│           ├── 📄 __init__.py           Tool registration hub
│           │                            - register_all_tools() function
│           │                            - Imports all tool modules
│           │
│           ├── 📄 system_info.py        System information tool
│           │                            - OS, hardware, CPU details
│           │                            - Memory and disk info
│           │                            - Python environment
│           │
│           ├── 📄 resource_monitor.py   Resource monitoring tool
│           │                            - CPU usage (overall & per-core)
│           │                            - Memory & swap usage
│           │                            - Disk & network I/O
│           │
│           ├── 📄 log_reader.py         Log file reader tool
│           │                            - Tail logs (last N lines)
│           │                            - Pattern filtering
│           │                            - Common log discovery
│           │
│           ├── 📄 network_diagnostic.py Network diagnostic tool
│           │                            - DNS resolution
│           │                            - Port connectivity
│           │                            - Connection timing
│           │
│           ├── 📄 process_search.py     Process search tool
│           │                            - Pattern-based search
│           │                            - CPU & memory usage
│           │                            - Process details
│           │
│           ├── 📄 environment_inspect.py Environment inspection tool
│           │                            - Environment variables
│           │                            - Development tool versions
│           │                            - PATH analysis
│           │
│           └── 📄 safe_command.py       Safe command execution tool
│                                        - Whitelisted commands only
│                                        - Timeout protection
│                                        - Output capture
│
├── 📁 docs/                             Documentation
│   │
│   ├── 📄 QUICKSTART.md                 5-minute setup guide
│   │                                    - Installation steps
│   │                                    - Configuration examples
│   │                                    - Quick validation
│   │
│   ├── 📄 EXAMPLES.md                   Detailed usage examples
│   │                                    - Example for each tool
│   │                                    - Multi-tool workflows
│   │                                    - Best practices
│   │
│   ├── 📄 CHANGELOG.md                  Version history
│   │                                    - Release notes
│   │                                    - Feature additions
│   │                                    - Breaking changes
│   │
│   ├── 📄 ARCHITECTURE.md               Technical architecture
│   │                                    - System design
│   │                                    - Component structure
│   │                                    - Security architecture
│   │
│   └── 📄 FOLDER_STRUCTURE.md           This file
│                                        - Complete structure reference
│                                        - File explanations
│
├── 📁 config/                           Configuration files
│   │
│   └── 📄 claude_desktop_config.example.json
│                                        Example Claude Desktop config
│                                        - macOS and Windows paths
│                                        - Multiple configuration methods
│
└── 📁 tests/                            Test suite
    │
    ├── 📄 __init__.py                   Test package initialization
    │
    └── 📄 test_server.py                Server validation tests
                                         - Python version check
                                         - Dependency validation
                                         - Import tests
                                         - psutil functionality tests
```

## 📋 File Count Summary

| Category | Count | Total Lines |
|----------|-------|-------------|
| **Python Modules** | 15 | ~1,500 |
| **Documentation** | 7 | ~3,000 |
| **Configuration** | 5 | ~200 |
| **Other** | 3 | ~100 |
| **Total** | **30 files** | **~4,800** |

## 🎯 Purpose of Each Folder

### `src/`
**Purpose:** Source code root following Python packaging standards
**Why:** Separates source from tests, docs, and config
**Contains:** Main package only

### `src/troubleshooting_mcp/`
**Purpose:** Main package with all application code
**Why:** Centralized, importable package
**Contains:** Core files + tools subfolder

### `src/troubleshooting_mcp/tools/`
**Purpose:** Individual diagnostic tool modules
**Why:** Modular design, easy to extend
**Contains:** 7 tool files + registration

### `docs/`
**Purpose:** All documentation (user & technical)
**Why:** Clean separation from code
**Contains:** 5 documentation files

### `config/`
**Purpose:** Configuration file examples
**Why:** Clear separation of config
**Contains:** Claude Desktop example config

### `tests/`
**Purpose:** Test suite and validation
**Why:** Standard Python test location
**Contains:** Test files

## 🔍 File Relationships

### Dependency Graph

```
troubleshooting_mcp.py (entry point)
    ↓
src/troubleshooting_mcp/server.py
    ↓
src/troubleshooting_mcp/tools/__init__.py
    ↓
src/troubleshooting_mcp/tools/{individual tools}
    ↓ (use)
src/troubleshooting_mcp/models.py
src/troubleshooting_mcp/utils.py
src/troubleshooting_mcp/constants.py
```

### Import Hierarchy

```
Level 1: Entry Points
  - troubleshooting_mcp.py
  - src/troubleshooting_mcp/server.py

Level 2: Registration
  - src/troubleshooting_mcp/tools/__init__.py

Level 3: Tool Implementations
  - src/troubleshooting_mcp/tools/*.py

Level 4: Support Modules
  - src/troubleshooting_mcp/models.py
  - src/troubleshooting_mcp/utils.py
  - src/troubleshooting_mcp/constants.py
```

## 📦 Package Structure

### What Gets Installed

When you run `pip install -e .`, these files are installed:
- ✅ All files in `src/troubleshooting_mcp/`
- ✅ Entry point script (`troubleshooting-mcp`)
- ✅ Dependencies (from requirements.txt)

### What Doesn't Get Installed

- ❌ Documentation (docs/)
- ❌ Tests (tests/)
- ❌ Root files (README, etc.)
- ❌ Config examples

## 🎨 Design Principles

### 1. Separation of Concerns
- Each tool in its own module
- Core functionality separated
- Utilities centralized

### 2. Discoverability
- Clear folder names
- Logical file organization
- Consistent naming

### 3. Extensibility
- Easy to add new tools
- Modular registration
- Clear patterns to follow

### 4. Professional Standards
- Follows PEP 518
- Standard Python structure
- Pip installable

## 🔄 How Files Interact

### Adding a New Tool

1. Create `src/troubleshooting_mcp/tools/new_tool.py`
2. Add input model to `src/troubleshooting_mcp/models.py`
3. Register in `src/troubleshooting_mcp/tools/__init__.py`
4. Use utilities from `utils.py`
5. Use constants from `constants.py`

### Modifying Configuration

1. Edit `src/troubleshooting_mcp/constants.py`
2. Changes apply to all tools automatically
3. No need to modify individual tools

### Updating Documentation

1. Edit files in `docs/` folder
2. Keep README.md in sync
3. Update CHANGELOG.md for changes

## 📊 Lines of Code by Component

| Component | Lines | Percentage |
|-----------|-------|------------|
| Tools | ~1,000 | 67% |
| Models | ~177 | 12% |
| Utils | ~73 | 5% |
| Server | ~24 | 2% |
| Constants | ~38 | 2% |
| Init files | ~50 | 3% |
| Setup files | ~138 | 9% |
| **Total Code** | **~1,500** | **100%** |

## 🎓 Learning the Structure

### For New Users
1. Start at project root
2. Read `README.md`
3. Check `docs/QUICKSTART.md`
4. Look at `src/troubleshooting_mcp/` structure

### For Developers
1. Study `docs/ARCHITECTURE.md`
2. Review tool implementations in `tools/`
3. Understand the registration pattern
4. Check shared utilities

### For Contributors
1. Understand the modular design
2. Follow existing patterns
3. Add tests in `tests/`
4. Update documentation in `docs/`

## 🚀 Quick Navigation

| I Want To... | Go To... |
|--------------|----------|
| Start using the server | `README.md` |
| Quick 5-min setup | `docs/QUICKSTART.md` |
| See usage examples | `docs/EXAMPLES.md` |
| Understand architecture | `docs/ARCHITECTURE.md` |
| Modify a tool | `src/troubleshooting_mcp/tools/` |
| Change configuration | `src/troubleshooting_mcp/constants.py` |
| Add validation | `src/troubleshooting_mcp/models.py` |
| Add utilities | `src/troubleshooting_mcp/utils.py` |
| Configure Claude | `config/claude_desktop_config.example.json` |
| Run tests | `tests/test_server.py` |

## 📈 Structure Evolution

### Version 1.0 (Current)
```
✅ Modular package structure
✅ Organized documentation
✅ Professional setup
✅ Backward compatible
```

### Future Versions
```
🔮 Plugin system
🔮 Config file support
🔮 Extended test suite
🔮 CI/CD integration
```

## 🎉 Summary

This structure provides:
- ✅ **Clear organization** - Easy to navigate
- ✅ **Modular design** - Easy to maintain
- ✅ **Professional standards** - Production ready
- ✅ **Good documentation** - Well explained
- ✅ **Easy to extend** - Clear patterns

---

**Last Updated:** 2025-01-05
**Version:** 1.0.0
**Status:** Production Ready

