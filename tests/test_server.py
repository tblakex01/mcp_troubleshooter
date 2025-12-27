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

def test_dependencies():
    """Verify all required packages are installed"""
    dependencies = {
        'mcp': 'mcp',
        'psutil': 'psutil',
        'pydantic': 'pydantic'
    }

    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
        except (ImportError, ModuleNotFoundError) as e:
            pytest.fail(f"{package} (not installed): {str(e)}")

def test_server_imports():
    """Verify the server file can be imported"""
    # Add src directory to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

    try:
        from troubleshooting_mcp import server
        assert hasattr(server, 'mcp'), "Server module missing 'mcp' attribute"
        assert hasattr(server, 'main'), "Server module missing 'main' function"
    except (ImportError, ModuleNotFoundError) as e:
        pytest.fail(f"Failed to import server module: {str(e)}")
    except AssertionError as e:
        pytest.fail(str(e))

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
