# Troubleshooting MCP Server - Architecture

This document describes the architecture and design decisions of the Troubleshooting MCP Server.

## Overview

The Troubleshooting MCP Server is designed as a modular, extensible system following best practices for Python package development. It provides diagnostic tools through the Model Context Protocol (MCP) to enable LLMs to help troubleshoot systems.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Desktop                        │
│                   (MCP Client)                           │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     │
┌────────────────────▼────────────────────────────────────┐
│               FastMCP Server                             │
│         (troubleshooting_mcp.server)                     │
├─────────────────────────────────────────────────────────┤
│                Tool Registration                         │
│         (register_all_tools function)                    │
├─────────────────────────────────────────────────────────┤
│                   Individual Tools                       │
│  ┌──────────┬──────────┬──────────┬──────────┐         │
│  │ System   │ Resource │ Log      │ Network  │         │
│  │ Info     │ Monitor  │ Reader   │ Diag     │         │
│  └──────────┴──────────┴──────────┴──────────┘         │
│  ┌──────────┬──────────┬──────────┐                    │
│  │ Process  │ Environ  │ Safe     │                    │
│  │ Search   │ Inspect  │ Command  │                    │
│  └──────────┴──────────┴──────────┘                    │
├─────────────────────────────────────────────────────────┤
│              Shared Components                           │
│  ┌──────────┬──────────┬──────────┬──────────┐         │
│  │ Models   │ Utils    │Constants │ Validation│         │
│  │(Pydantic)│(Helpers) │(Config)  │(Security) │         │
│  └──────────┴──────────┴──────────┴──────────┘         │
├─────────────────────────────────────────────────────────┤
│               System Interface                           │
│  ┌──────────┬──────────┬──────────┬──────────┐         │
│  │ psutil   │ socket   │subprocess│ os/sys   │         │
│  │(Metrics) │(Network) │(Commands)│(Environ) │         │
│  └──────────┴──────────┴──────────┴──────────┘         │
└─────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Operating System                            │
│     (Linux / macOS / Windows)                           │
└─────────────────────────────────────────────────────────┘
```

## Component Structure

### 1. Entry Points

#### `troubleshooting_mcp.py` (Root)
- **Purpose**: Backward compatibility wrapper
- **Function**: Imports and runs the modular server
- **Use Case**: For users with existing Claude Desktop configurations

#### `src/troubleshooting_mcp/server.py`
- **Purpose**: Main server entry point
- **Function**: Initializes FastMCP server and registers all tools
- **Exports**: `main()` function for console script

### 2. Core Components

#### `src/troubleshooting_mcp/__init__.py`
- Package initialization
- Exports the MCP server instance
- Defines version, author, license

#### `src/troubleshooting_mcp/constants.py`
- **CHARACTER_LIMIT**: Maximum response size (25,000 chars)
- **SAFE_COMMANDS**: Whitelist of executable commands
- **COMMON_LOG_PATHS**: System log file locations

#### `src/troubleshooting_mcp/models.py`
- **ResponseFormat**: Enum for output formats (Markdown/JSON)
- **Input Models**: Pydantic models for each tool
  - SystemInfoInput
  - ResourceMonitorInput
  - LogFileInput
  - NetworkDiagnosticInput
  - ProcessSearchInput
  - EnvironmentSearchInput
  - SafeCommandInput

#### `src/troubleshooting_mcp/utils.py`
- **format_bytes()**: Convert bytes to human-readable format
- **format_timestamp()**: Convert Unix timestamp to datetime
- **handle_error()**: Consistent error formatting
- **check_character_limit()**: Enforce response size limits

### 3. Tools (src/troubleshooting_mcp/tools/)

Each tool is self-contained in its own module with a registration function:

#### `system_info.py`
- Gathers OS, hardware, CPU, memory, disk info
- Uses: platform, psutil
- Returns: Markdown or JSON

#### `resource_monitor.py`
- Real-time CPU, memory, swap, disk I/O, network I/O
- Uses: psutil
- Optional per-CPU statistics

#### `log_reader.py`
- Reads last N lines from log files
- Pattern-based filtering
- Lists common log locations

#### `network_diagnostic.py`
- DNS resolution testing
- TCP port connectivity checks
- Connection timing

#### `process_search.py`
- Search processes by pattern
- CPU and memory usage
- Sorted by resource consumption

#### `environment_inspect.py`
- Environment variable listing
- Development tool version detection
- Pattern-based filtering

#### `safe_command.py`
- Whitelisted command execution
- Timeout protection
- Command output capture

## Design Patterns

### 1. Modular Tool Registration

Each tool follows this pattern:

```python
def register_tool_name(mcp):
    @mcp.tool(name="tool_name", annotations={...})
    async def tool_name(params: InputModel) -> str:
        try:
            # Implementation
            return result
        except Exception as e:
            return handle_error(e)
```

**Benefits:**
- Easy to add new tools
- Consistent error handling
- Clear separation of concerns
- Testable in isolation

### 2. Pydantic Input Validation

All inputs are validated using Pydantic v2:

```python
class ToolInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
    param: str = Field(..., description="...")
```

**Benefits:**
- Type safety
- Automatic validation
- Clear error messages
- Self-documenting API

### 3. Dual Output Format

Most tools support both Markdown and JSON:

```python
if params.response_format == ResponseFormat.MARKDOWN:
    return format_as_markdown(data)
else:
    return json.dumps(data, indent=2)
```

**Benefits:**
- Human-readable for interactive use
- Machine-readable for automation
- Flexible integration

### 4. Security by Design

Multiple security layers:

```python
# 1. Command whitelist
if command not in SAFE_COMMANDS:
    raise ValueError("Not whitelisted")

# 2. Input validation
@field_validator('command')
def validate_command(cls, v: str) -> str:
    # Validation logic

# 3. Timeout protection
subprocess.run(..., timeout=params.timeout)

# 4. Permission handling
if not os.access(file, os.R_OK):
    return "Permission denied"
```

## Data Flow

### Example: Network Connectivity Test

1. **User Query**: "Can I reach google.com on port 443?"
2. **Claude Desktop**: Parses intent, calls MCP tool
3. **MCP Server**: Routes to `troubleshooting_test_network_connectivity`
4. **Input Validation**: Pydantic validates host, port, timeout
5. **DNS Resolution**: socket.gethostbyname('google.com')
6. **Port Test**: socket.connect((ip, port))
7. **Timing Measurement**: Records connection time
8. **Format Response**: Markdown with status indicators
9. **Return to Client**: Through MCP protocol
10. **Display to User**: In Claude interface

## Security Architecture

### Multi-Layer Security

1. **Input Layer**
   - Pydantic validation
   - Type checking
   - Range constraints
   - Pattern validation

2. **Execution Layer**
   - Command whitelist
   - Timeout protection
   - Permission checks
   - No privilege escalation

3. **Output Layer**
   - Character limit enforcement
   - Safe error messages
   - No sensitive data leakage

### Threat Model

**Threats Addressed:**
- ❌ Arbitrary command execution → Whitelist only
- ❌ Resource exhaustion → Timeout limits
- ❌ Unauthorized file access → Permission checks
- ❌ Data exfiltration → Character limits
- ❌ Code injection → Input validation

**Threats NOT Addressed:**
- Physical access to machine
- OS-level vulnerabilities
- Network-layer attacks
- Compromised Python runtime

## Extension Points

### Adding New Tools

1. Create module in `src/troubleshooting_mcp/tools/`
2. Define Pydantic input model
3. Implement registration function
4. Add to `register_all_tools()`

### Adding New Utilities

1. Add function to `src/troubleshooting_mcp/utils.py`
2. Import in tool modules as needed
3. Keep utilities generic and reusable

### Adding New Constants

1. Add to `src/troubleshooting_mcp/constants.py`
2. Import where needed
3. Document purpose and format

## Performance Considerations

### Response Times

| Operation | Expected Time |
|-----------|--------------|
| System Info | < 1s |
| Resource Monitor | 1-2s (CPU sampling) |
| Log Read (50 lines) | < 1s |
| Network Test | 5-10s (with DNS) |
| Process Search | 1-3s |
| Environment Inspect | 2-5s (tool checks) |
| Command Execution | Varies (0-300s) |

### Memory Usage

- Base server: ~50MB
- Per request: ~1-5MB
- Log reading: Efficient tail-like approach
- Process enumeration: Streaming with psutil

### Optimization Strategies

1. **Lazy Imports**: Import heavy modules only when needed
2. **Efficient Reading**: Tail logs from end, don't load full file
3. **Streaming**: Process large datasets in chunks
4. **Caching**: Reuse expensive operations where appropriate
5. **Timeouts**: Prevent hanging operations

## Testing Strategy

### Unit Tests
- Test each utility function
- Test input validation models
- Test error handling

### Integration Tests
- Test each tool end-to-end
- Test MCP protocol communication
- Test cross-platform compatibility

### Validation Tests
- `tests/test_server.py` validates setup
- Checks dependencies
- Verifies imports
- Tests psutil functionality

## Deployment Models

### 1. Direct Execution
```bash
python troubleshooting_mcp.py
```
Best for: Quick testing, development

### 2. Module Execution
```bash
python -m troubleshooting_mcp.server
```
Best for: Python package best practices

### 3. Installed Package
```bash
pip install -e .
troubleshooting-mcp
```
Best for: Production use, system-wide access

### 4. Docker Container
```dockerfile
FROM python:3.10-slim
COPY . /app
RUN pip install /app
CMD ["troubleshooting-mcp"]
```
Best for: Isolated environments, cloud deployment

## Future Architecture Enhancements

### Planned Improvements

1. **Plugin System**: Dynamic tool loading
2. **Configuration File**: YAML/TOML for settings
3. **Caching Layer**: Redis for expensive operations
4. **Metrics Collection**: Prometheus integration
5. **Authentication**: API key support
6. **Multi-Host**: Query multiple servers
7. **Async I/O**: Full async/await throughout

### Scalability Considerations

- Stateless design enables horizontal scaling
- Each request is independent
- No shared state between invocations
- Can run multiple instances

## Conclusion

The Troubleshooting MCP Server is designed with:
- **Modularity**: Easy to extend and maintain
- **Security**: Multiple defensive layers
- **Usability**: Clear APIs and documentation
- **Reliability**: Comprehensive error handling
- **Performance**: Efficient operations

This architecture supports both current needs and future growth.

