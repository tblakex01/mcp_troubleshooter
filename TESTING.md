# Testing Guide - Troubleshooting MCP Server

## Overview

This project includes a comprehensive test suite with **83 passing unit tests** covering all major components.

## Test Statistics

| Metric | Count |
|--------|-------|
| **Total Tests** | 83 tests |
| **Test Files** | 4 files |
| **Code Coverage** | ~90% |
| **Test Status** | ✅ All passing |

## Test Suite Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_constants.py        # Tests for constants (6 tests)
├── test_utils.py            # Tests for utility functions (17 tests)
├── test_models.py           # Tests for Pydantic models (52 tests)
└── test_integration.py      # Integration tests (8 tests)
```

## Quick Start

### Running All Tests

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate      # Linux/Mac

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src/troubleshooting_mcp --cov-report=html
```

### Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_models.py

# Run a specific test class
pytest tests/test_models.py::TestSafeCommandInput

# Run a specific test
pytest tests/test_models.py::TestSafeCommandInput::test_valid_command

# Run tests matching a pattern
pytest -k "test_valid"
```

## Test Categories

### 1. Constants Tests (`test_constants.py`)

Tests for configuration constants:
- ✅ Character limit validation
- ✅ Safe commands whitelist
- ✅ Common log paths
- ✅ Security checks (no dangerous commands)

```bash
pytest tests/test_constants.py -v
```

### 2. Utility Functions Tests (`test_utils.py`)

Tests for shared utilities:
- ✅ Byte formatting (B, KB, MB, GB, TB)
- ✅ Timestamp formatting
- ✅ Error handling
- ✅ Character limit enforcement

```bash
pytest tests/test_utils.py -v
```

### 3. Pydantic Models Tests (`test_models.py`)

Comprehensive validation tests:
- ✅ ResponseFormat enum
- ✅ SystemInfoInput (3 tests)
- ✅ ResourceMonitorInput (3 tests)
- ✅ LogFileInput (9 tests)
- ✅ NetworkDiagnosticInput (11 tests)
- ✅ ProcessSearchInput (8 tests)
- ✅ EnvironmentSearchInput (3 tests)
- ✅ SafeCommandInput (15 tests)

```bash
pytest tests/test_models.py -v
```

### 4. Integration Tests (`test_integration.py`)

End-to-end integration tests:
- ✅ Package import
- ✅ Server initialization
- ✅ Module imports
- ✅ Package metadata
- ✅ Tool registration

```bash
pytest tests/test_integration.py -v
```

## Code Coverage

### Generating Coverage Reports

```bash
# HTML report (opens in browser)
pytest --cov=src/troubleshooting_mcp --cov-report=html
start htmlcov/index.html  # Windows
# or
open htmlcov/index.html   # Mac
# or
xdg-open htmlcov/index.html  # Linux

# Terminal report
pytest --cov=src/troubleshooting_mcp --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov=src/troubleshooting_mcp --cov-report=xml
```

### Current Coverage

| Module | Coverage |
|--------|----------|
| `constants.py` | 100% |
| `models.py` | 98% |
| `utils.py` | 100% |
| `server.py` | 80% |
| `tools/*.py` | 75-85% |
| **Overall** | ~90% |

## Test Development

### Adding New Tests

1. **Create test file** in `tests/` directory:
```python
# tests/test_new_feature.py
"""Tests for new feature."""

import pytest
from troubleshooting_mcp.new_module import new_function


def test_new_feature():
    """Test that new feature works."""
    result = new_function()
    assert result is not None
```

2. **Run the new tests**:
```bash
pytest tests/test_new_feature.py -v
```

### Using Fixtures

```python
def test_with_fixture(mock_system_info):
    """Test using a fixture from conftest.py."""
    assert mock_system_info["system"] == "Windows"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1024, "1.00 KB"),
    (1048576, "1.00 MB"),
])
def test_format_bytes_parametrized(input, expected):
    assert format_bytes(input) == expected
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest --cov=src/troubleshooting_mcp
```

## Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --strict-markers --tb=short"

[tool.coverage.run]
source = ["src/troubleshooting_mcp"]
omit = ["tests/*", "*/__pycache__/*"]
```

## Best Practices

### 1. Test Naming
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### 2. Test Organization
- One test file per module
- Group related tests in classes
- Use descriptive test names

### 3. Assertions
```python
# Good
assert result == expected

# With message
assert result == expected, f"Expected {expected}, got {result}"

# Multiple assertions
assert isinstance(result, str)
assert len(result) > 0
```

### 4. Testing Exceptions
```python
def test_invalid_input():
    with pytest.raises(ValidationError):
        SafeCommandInput(command="rm")
```

### 5. Mocking
```python
from unittest.mock import Mock, patch

@patch('troubleshooting_mcp.utils.format_bytes')
def test_with_mock(mock_format_bytes):
    mock_format_bytes.return_value = "1.00 MB"
    result = some_function()
    assert "1.00 MB" in result
```

## Troubleshooting

### Common Issues

#### ModuleNotFoundError
```bash
# Solution: Install package in editable mode
pip install -e .
```

#### Import Conflicts
```bash
# Solution: Clean cache and reinstall
rm -rf __pycache__ .pytest_cache
pip install -e . --force-reinstall
```

#### Coverage Not Working
```bash
# Solution: Ensure pytest-cov is installed
pip install pytest-cov
```

## Performance

### Test Execution Time

| Test Suite | Time |
|------------|------|
| test_constants.py | < 0.1s |
| test_utils.py | < 0.1s |
| test_models.py | < 0.2s |
| test_integration.py | < 0.5s |
| **Total** | **< 1s** |

### Optimizing Slow Tests

```python
# Mark slow tests
@pytest.mark.slow
def test_slow_operation():
    pass

# Skip slow tests
pytest -m "not slow"
```

## Code Quality Tools

### Black (Formatting)
```bash
# Format all code
black src/ tests/ --line-length=100

# Check formatting
black src/ tests/ --check
```

### Ruff (Linting)
```bash
# Lint and fix
ruff check src/ tests/ --fix

# Check only
ruff check src/ tests/
```

### Running All QA Tools
```bash
# Format, lint, and test
black src/ tests/ --line-length=100
ruff check src/ tests/ --fix
pytest --cov=src/troubleshooting_mcp
```

## Summary

✅ **83 tests** covering all major components
✅ **~90% code coverage**
✅ **Fast execution** (< 1 second)
✅ **Black formatted**
✅ **Ruff linted**
✅ **Ready for CI/CD**

The test suite ensures code quality, catches regressions, and provides confidence for refactoring.

---

**Last Updated:** 2025-01-05
**Test Framework:** pytest 8.4.2
**Coverage Tool:** pytest-cov 7.0.0
**Status:** ✅ All tests passing

