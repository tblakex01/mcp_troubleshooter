"""
Pytest configuration and shared fixtures for Troubleshooting MCP Server tests.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_system_info():
    """Mock system information data."""
    return {
        "system": "Windows",
        "node_name": "test-machine",
        "release": "10",
        "version": "10.0.26200",
        "machine": "AMD64",
        "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel",
        "boot_time": "2025-01-05 10:00:00",
        "python_version": "3.12.0",
        "python_executable": "/usr/bin/python3",
    }


@pytest.fixture
def mock_process_data():
    """Mock process data."""
    return [
        {
            "pid": 1234,
            "name": "python",
            "cpu_percent": 5.2,
            "memory_bytes": 104857600,
            "memory_formatted": "100.00 MB",
            "status": "running",
            "cmdline": "python test.py",
        }
    ]


@pytest.fixture
def sample_log_content():
    """Sample log file content."""
    return """2025-01-05 10:00:00 INFO Starting application
2025-01-05 10:00:01 DEBUG Loading configuration
2025-01-05 10:00:02 ERROR Connection failed
2025-01-05 10:00:03 WARNING Retrying connection
2025-01-05 10:00:04 INFO Application started successfully
"""

@pytest.fixture(autouse=True)
def mock_allowed_log_dirs(monkeypatch, tmp_path):
    """
    Mock ALLOWED_LOG_DIRS to include the temporary directory used by tests.
    This ensures that LogReaderTool tests pass in the restricted environment.
    """
    # Patch the constants module
    from troubleshooting_mcp import constants
    original_dirs = constants.ALLOWED_LOG_DIRS
    new_dirs = original_dirs + [str(tmp_path), "/tmp"]
    monkeypatch.setattr(constants, "ALLOWED_LOG_DIRS", new_dirs)

    # Also patch the log_reader module where it's imported
    # We need to try/except because it might not be imported yet
    try:
        from troubleshooting_mcp.tools import log_reader
        monkeypatch.setattr(log_reader, "ALLOWED_LOG_DIRS", new_dirs)
    except ImportError:
        pass
