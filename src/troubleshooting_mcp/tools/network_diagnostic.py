"""
Network Diagnostic Tool - Test network connectivity.
"""

import socket
from datetime import datetime

from ..models import NetworkDiagnosticInput
from ..utils import handle_error


def register_network_diagnostic(mcp):
    """Register the network diagnostic tool with the MCP server."""

    @mcp.tool(
        name="troubleshooting_test_network_connectivity",
        annotations={
            "title": "Test Network Connectivity",
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True,
        },
    )
    async def troubleshooting_test_network_connectivity(params: NetworkDiagnosticInput) -> str:
        """Test network connectivity to a host and optionally a specific port.

        This tool performs network connectivity tests including DNS resolution and
        TCP connection tests to verify that a host is reachable. It can test both
        basic hostname resolution and specific service ports.

        Args:
            params (NetworkDiagnosticInput): Validated input parameters containing:
                - host (str): Hostname or IP address to test (e.g., 'google.com', '8.8.8.8')
                - port (Optional[int]): Port number to test (e.g., 80, 443, 22)
                - timeout (Optional[int]): Timeout in seconds (default: 5, max: 30)

        Returns:
            str: Markdown-formatted connectivity test results

            Success response includes:
            - DNS resolution status and IP address
            - Port connectivity status (if port specified)
            - Response time measurements

            Error response:
            - "Error: Cannot resolve hostname" if DNS fails
            - "Error: Connection refused" if port is closed
            - "Error: Connection timeout" if host is unreachable

        Examples:
            - Use when: "Is google.com reachable?"
            - Use when: "Test if port 443 is open on example.com"
            - Use when: "Check connectivity to 192.168.1.1"
            - Use when: "Verify SSH access to server.example.com port 22"

        Error Handling:
            - Returns detailed error for DNS resolution failures
            - Returns connection status for port tests
            - Handles timeout scenarios with clear messaging
        """
        try:
            result_lines = ["# Network Connectivity Test", f"**Host:** {params.host}", ""]

            # DNS Resolution Test
            start_time = datetime.now()
            try:
                ip_address = socket.gethostbyname(params.host)
                dns_time = (datetime.now() - start_time).total_seconds() * 1000
                result_lines.append("✓ **DNS Resolution:** Success")
                result_lines.append(f"  - IP Address: {ip_address}")
                result_lines.append(f"  - Resolution Time: {dns_time:.2f}ms")
            except socket.gaierror:
                result_lines.append("✗ **DNS Resolution:** Failed")
                result_lines.append(f"  - Error: Cannot resolve hostname '{params.host}'")
                return "\n".join(result_lines)

            result_lines.append("")

            # Port Connectivity Test (if port specified)
            if params.port:
                result_lines.append(f"**Port Test:** {params.port}")
                start_time = datetime.now()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(params.timeout)

                try:
                    sock.connect((ip_address, params.port))
                    connect_time = (datetime.now() - start_time).total_seconds() * 1000
                    result_lines.append("✓ **Connection:** Success")
                    result_lines.append(f"  - Port {params.port} is OPEN")
                    result_lines.append(f"  - Connection Time: {connect_time:.2f}ms")
                except TimeoutError:
                    result_lines.append("✗ **Connection:** Timeout")
                    result_lines.append(
                        f"  - Port {params.port} did not respond within {params.timeout}s"
                    )
                except ConnectionRefusedError:
                    result_lines.append("✗ **Connection:** Refused")
                    result_lines.append(f"  - Port {params.port} is CLOSED or filtered")
                except Exception as e:
                    result_lines.append("✗ **Connection:** Failed")
                    result_lines.append(f"  - Error: {str(e)}")
                finally:
                    sock.close()
            else:
                result_lines.append(
                    "*No port specified. Use 'port' parameter to test specific services.*"
                )

            return "\n".join(result_lines)

        except Exception as e:
            return handle_error(e)
