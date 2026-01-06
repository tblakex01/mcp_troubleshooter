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
            print(f"  ✓ {package}")
        except (ImportError, ModuleNotFoundError) as e:
            pytest.fail(f"{package} (not installed): {str(e)}")

def test_server_imports():
    """Verify the server file can be imported"""
    print("\nTesting server imports...", end=" ")
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    try:
        from troubleshooting_mcp import server
        assert hasattr(server, 'mcp'), "Server module missing 'mcp' attribute"
        assert hasattr(server, 'main'), "Server module missing 'main' function"
        print("✓")
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

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)

    passed = sum(results.values())
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status}: {test_name}")

    print("="*50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed! Server is ready to use.")
        print("\nNext steps:")
        print("1. Review QUICKSTART.md for configuration instructions")
        print("2. Add server to Claude Desktop config")
        print("3. Restart Claude Desktop")
        return True
    else:
        print("\n✗ Some tests failed. Please resolve issues before proceeding.")
        print("\nTo fix issues:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Verify Python version is 3.10 or higher")
        print("3. Check that troubleshooting_mcp.py is in the current directory")
        return False

def run_test_safe(test_func):
    """Run a test function and return True if it passes, False otherwise"""
    try:
        test_func()
        return True
    except Exception:
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("TROUBLESHOOTING MCP SERVER - TEST SUITE")
    print("="*50)

    results = {
        "Python Version": run_test_safe(test_python_version),
        "Dependencies": run_test_safe(test_dependencies),
        "Server Imports": run_test_safe(test_server_imports),
        "psutil Functionality": run_test_safe(test_psutil_functionality),
        "Pydantic Validation": run_test_safe(test_pydantic_models),
        "Command Availability": run_test_safe(test_command_availability)
    }

    success = print_summary(results)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
