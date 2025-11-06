"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError

from troubleshooting_mcp.models import (
    EnvironmentSearchInput,
    LogFileInput,
    NetworkDiagnosticInput,
    ProcessSearchInput,
    ResourceMonitorInput,
    ResponseFormat,
    SafeCommandInput,
    SystemInfoInput,
)


class TestResponseFormat:
    """Tests for ResponseFormat enum."""

    def test_markdown_format(self):
        assert ResponseFormat.MARKDOWN == "markdown"

    def test_json_format(self):
        assert ResponseFormat.JSON == "json"


class TestSystemInfoInput:
    """Tests for SystemInfoInput model."""

    def test_valid_markdown_format(self):
        model = SystemInfoInput(response_format="markdown")
        assert model.response_format == ResponseFormat.MARKDOWN

    def test_valid_json_format(self):
        model = SystemInfoInput(response_format="json")
        assert model.response_format == ResponseFormat.JSON

    def test_default_format(self):
        model = SystemInfoInput()
        assert model.response_format == ResponseFormat.MARKDOWN


class TestResourceMonitorInput:
    """Tests for ResourceMonitorInput model."""

    def test_with_per_cpu(self):
        model = ResourceMonitorInput(include_per_cpu=True)
        assert model.include_per_cpu is True

    def test_default_per_cpu(self):
        model = ResourceMonitorInput()
        assert model.include_per_cpu is False

    def test_with_response_format(self):
        model = ResourceMonitorInput(response_format="json")
        assert model.response_format == ResponseFormat.JSON


class TestLogFileInput:
    """Tests for LogFileInput model."""

    def test_with_file_path(self):
        model = LogFileInput(file_path="/var/log/syslog")
        assert model.file_path == "/var/log/syslog"

    def test_without_file_path(self):
        model = LogFileInput()
        assert model.file_path is None

    def test_valid_lines_count(self):
        model = LogFileInput(lines=100)
        assert model.lines == 100

    def test_lines_minimum_boundary(self):
        model = LogFileInput(lines=1)
        assert model.lines == 1

    def test_lines_maximum_boundary(self):
        model = LogFileInput(lines=1000)
        assert model.lines == 1000

    def test_lines_below_minimum(self):
        with pytest.raises(ValidationError):
            LogFileInput(lines=0)

    def test_lines_above_maximum(self):
        with pytest.raises(ValidationError):
            LogFileInput(lines=1001)

    def test_with_search_pattern(self):
        model = LogFileInput(search_pattern="error")
        assert model.search_pattern == "error"

    def test_file_path_too_long(self):
        with pytest.raises(ValidationError):
            LogFileInput(file_path="x" * 501)


class TestNetworkDiagnosticInput:
    """Tests for NetworkDiagnosticInput model."""

    def test_valid_hostname(self):
        model = NetworkDiagnosticInput(host="google.com")
        assert model.host == "google.com"

    def test_valid_ip_address(self):
        model = NetworkDiagnosticInput(host="8.8.8.8")
        assert model.host == "8.8.8.8"

    def test_with_port(self):
        model = NetworkDiagnosticInput(host="example.com", port=443)
        assert model.port == 443

    def test_port_minimum(self):
        model = NetworkDiagnosticInput(host="example.com", port=1)
        assert model.port == 1

    def test_port_maximum(self):
        model = NetworkDiagnosticInput(host="example.com", port=65535)
        assert model.port == 65535

    def test_port_below_minimum(self):
        with pytest.raises(ValidationError):
            NetworkDiagnosticInput(host="example.com", port=0)

    def test_port_above_maximum(self):
        with pytest.raises(ValidationError):
            NetworkDiagnosticInput(host="example.com", port=65536)

    def test_empty_host(self):
        with pytest.raises(ValidationError):
            NetworkDiagnosticInput(host="")

    def test_whitespace_host_stripped(self):
        model = NetworkDiagnosticInput(host="  google.com  ")
        assert model.host == "google.com"

    def test_timeout_default(self):
        model = NetworkDiagnosticInput(host="example.com")
        assert model.timeout == 5

    def test_timeout_custom(self):
        model = NetworkDiagnosticInput(host="example.com", timeout=10)
        assert model.timeout == 10


class TestProcessSearchInput:
    """Tests for ProcessSearchInput model."""

    def test_with_pattern(self):
        model = ProcessSearchInput(pattern="python")
        assert model.pattern == "python"

    def test_without_pattern(self):
        model = ProcessSearchInput()
        assert model.pattern is None

    def test_limit_default(self):
        model = ProcessSearchInput()
        assert model.limit == 20

    def test_limit_custom(self):
        model = ProcessSearchInput(limit=50)
        assert model.limit == 50

    def test_limit_minimum(self):
        model = ProcessSearchInput(limit=1)
        assert model.limit == 1

    def test_limit_maximum(self):
        model = ProcessSearchInput(limit=100)
        assert model.limit == 100

    def test_limit_below_minimum(self):
        with pytest.raises(ValidationError):
            ProcessSearchInput(limit=0)

    def test_limit_above_maximum(self):
        with pytest.raises(ValidationError):
            ProcessSearchInput(limit=101)


class TestEnvironmentSearchInput:
    """Tests for EnvironmentSearchInput model."""

    def test_with_pattern(self):
        model = EnvironmentSearchInput(pattern="PATH")
        assert model.pattern == "PATH"

    def test_without_pattern(self):
        model = EnvironmentSearchInput()
        assert model.pattern is None

    def test_response_format(self):
        model = EnvironmentSearchInput(response_format="json")
        assert model.response_format == ResponseFormat.JSON


class TestSafeCommandInput:
    """Tests for SafeCommandInput model."""

    def test_valid_command(self):
        model = SafeCommandInput(command="ping")
        assert model.command == "ping"

    def test_command_case_insensitive(self):
        model = SafeCommandInput(command="PING")
        assert model.command == "ping"

    def test_invalid_command(self):
        with pytest.raises(ValidationError) as exc_info:
            SafeCommandInput(command="rm")
        assert "not in the whitelist" in str(exc_info.value)

    def test_with_args(self):
        model = SafeCommandInput(command="ping", args=["-c", "4", "google.com"])
        assert model.args == ["-c", "4", "google.com"]

    def test_without_args(self):
        model = SafeCommandInput(command="uptime")
        assert model.args == []

    def test_timeout_default(self):
        model = SafeCommandInput(command="ping")
        assert model.timeout == 30

    def test_timeout_custom(self):
        model = SafeCommandInput(command="ping", timeout=60)
        assert model.timeout == 60

    def test_timeout_minimum(self):
        model = SafeCommandInput(command="ping", timeout=1)
        assert model.timeout == 1

    def test_timeout_maximum(self):
        model = SafeCommandInput(command="ping", timeout=300)
        assert model.timeout == 300

    def test_timeout_below_minimum(self):
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", timeout=0)

    def test_timeout_above_maximum(self):
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", timeout=301)

    def test_too_many_args(self):
        with pytest.raises(ValidationError):
            SafeCommandInput(command="ping", args=["arg"] * 21)
