#!/usr/bin/env python3
"""
Test script for Troubleshooting MCP Server

This script verifies that all dependencies are installed correctly and that
the server can initialize properly. Run this before configuring Claude Desktop
to ensure everything works.

Usage:
    python test_server.py
"""

import os
import sys
import pytest


def test_python_version():
    """Verify Python version is 3.10+"""
    version = sys.version_info
    assert version.major >= 3 and version.minor >= 10, \
        f"Python {version.major}.{version.minor}.{version.micro} is below required 3.10+"

@pytest.mark.parametrize("package,import_name", [
    ('mcp', 'mcp'),
    ('psutil', 'psutil'),
    ('pydantic', 'pydantic'),
])
def test_dependencies(package, import_name):
    """Verify all required packages are installed"""
    try:
        __import__(import_name)
    except ImportError:
        pytest.fail(f"{package} is not installed")

def test_server_imports():
    """Verify the server file can be imported"""
    try:
        from src.troubleshooting_mcp.server import main, mcp
        assert mcp is not None, "Server module missing 'mcp' attribute"
        assert callable(main), "Server module 'main' is not callable"
    except ImportError as e:
        pytest.fail(f"Failed to import server module: {str(e)}")

def test_psutil_functionality():
    """Verify psutil can access system information"""
    import psutil

    # Test CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    assert cpu_percent >= 0.0

    # Test memory
    mem = psutil.virtual_memory()
    assert mem.percent >= 0.0

    # Test disk
    disk = psutil.disk_usage('/')
    assert disk.percent >= 0.0

    # Test processes
    process_count = len(list(psutil.process_iter()))
    assert process_count > 0

def test_pydantic_models():
    """Verify Pydantic models work correctly"""
    from pydantic import BaseModel, ConfigDict, Field, ValidationError
    import pytest

    class TestModel(BaseModel):
        model_config = ConfigDict(
            str_strip_whitespace=True,
            validate_assignment=True
        )
        test_field: str = Field(..., min_length=1)

    # Test valid input
    model = TestModel(test_field="test")
    assert model.test_field == "test"

    # Test validation should fail for empty string
    with pytest.raises(ValidationError):
        TestModel(test_field="")

def test_command_availability():
    """Test availability of common diagnostic commands"""
    import shutil

    commands = ['ping', 'netstat', 'df', 'free', 'uptime']
    available = [cmd for cmd in commands if shutil.which(cmd)]

    # At least some commands should be available on most systems
    assert len(available) > 0, "No diagnostic commands found on system"

def main():
    """Run all tests using pytest"""
    print("="*50)
    print("TROUBLESHOOTING MCP SERVER - TEST SUITE")
    print("="*50)
    print("\nRunning tests with pytest...\n")

    # Run pytest with verbose output
    exit_code = pytest.main([__file__, '-v', '--tb=short'])

    if exit_code == 0:
        print("\n✓ All tests passed! Server is ready to use.")
        print("\nNext steps:")
        print("1. Review QUICKSTART.md for configuration instructions")
        print("2. Add server to Claude Desktop config")
        print("3. Restart Claude Desktop")
    else:
        print("\n✗ Some tests failed. Please resolve issues before proceeding.")
        print("\nTo fix issues:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Verify Python version is 3.10 or higher")
        print("3. Check that troubleshooting_mcp package is installed")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
