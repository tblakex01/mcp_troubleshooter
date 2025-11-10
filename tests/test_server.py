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
    print("Testing Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.10+)")
        return False

def test_dependencies():
    """Verify all required packages are installed"""
    print("\nTesting dependencies...")
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

    return True

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
        return True
    except (ImportError, ModuleNotFoundError) as e:
        pytest.fail(f"Failed to import server module: {str(e)}")
    except AssertionError as e:
        pytest.fail(str(e))

def test_psutil_functionality():
    """Verify psutil can access system information"""
    print("\nTesting psutil functionality...")
    try:
        import psutil

        # Test CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        print(f"  ✓ CPU monitoring (current: {cpu_percent}%)")

        # Test memory
        mem = psutil.virtual_memory()
        print(f"  ✓ Memory monitoring (used: {mem.percent}%)")

        # Test disk
        disk = psutil.disk_usage('/')
        print(f"  ✓ Disk monitoring (used: {disk.percent}%)")

        # Test processes
        process_count = len(list(psutil.process_iter()))
        print(f"  ✓ Process monitoring ({process_count} processes)")

        return True
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def test_pydantic_models():
    """Verify Pydantic models work correctly"""
    print("\nTesting Pydantic validation...", end=" ")
    try:
        from pydantic import BaseModel, ConfigDict, Field

        class TestModel(BaseModel):
            model_config = ConfigDict(
                str_strip_whitespace=True,
                validate_assignment=True
            )
            test_field: str = Field(..., min_length=1)

        # Test valid input
        model = TestModel(test_field="test")

        # Test validation
        try:
            TestModel(test_field="")
        except:
            pass  # Expected to fail

        print("✓")
        return True
    except Exception as e:
        print(f"✗\n  Error: {str(e)}")
        return False

def test_command_availability():
    """Test availability of common diagnostic commands"""
    print("\nTesting diagnostic command availability...")
    import shutil

    commands = ['ping', 'netstat', 'df', 'free', 'uptime']
    available = []
    unavailable = []

    for cmd in commands:
        if shutil.which(cmd):
            available.append(cmd)
            print(f"  ✓ {cmd}")
        else:
            unavailable.append(cmd)
            print(f"  - {cmd} (not found)")

    if len(available) > 0:
        print(f"\n  {len(available)}/{len(commands)} diagnostic commands available")
        return True
    else:
        print("\n  Warning: No diagnostic commands found")
        return False

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

def main():
    """Run all tests"""
    print("="*50)
    print("TROUBLESHOOTING MCP SERVER - TEST SUITE")
    print("="*50)

    results = {
        "Python Version": test_python_version(),
        "Dependencies": test_dependencies(),
        "Server Imports": test_server_imports(),
        "psutil Functionality": test_psutil_functionality(),
        "Pydantic Validation": test_pydantic_models(),
        "Command Availability": test_command_availability()
    }

    success = print_summary(results)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
