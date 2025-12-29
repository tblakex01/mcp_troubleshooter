
import pytest
from pydantic import ValidationError
from troubleshooting_mcp.models import SafeCommandInput

def test_ip_command_security_restrictions():
    """
    Verify that SafeCommandInput BLOCKS dangerous 'ip' arguments.
    """
    # Verify that 'ip netns exec' (Command Injection) is blocked
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ip", args=["netns", "exec", "default", "rm", "-rf", "/"])
    assert "Argument 'netns' is not allowed" in str(excinfo.value)

    # Verify that 'ip link set down' (Destructive) is blocked
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ip", args=["link", "set", "eth0", "down"])
    assert "Operation 'link set' is not allowed" in str(excinfo.value)

    # Verify safe usage still works
    safe_input = SafeCommandInput(command="ip", args=["addr", "show"])
    assert safe_input.command == "ip"
    assert safe_input.args == ["addr", "show"]

def test_ifconfig_security_restrictions():
    """
    Verify that SafeCommandInput BLOCKS dangerous 'ifconfig' arguments.
    """
    # Verify that 'ifconfig down' (Destructive) is blocked
    with pytest.raises(ValidationError) as excinfo:
        SafeCommandInput(command="ifconfig", args=["eth0", "down"])
    assert "State changing arguments" in str(excinfo.value)

    # Verify safe usage still works
    safe_input = SafeCommandInput(command="ifconfig", args=["-a"])
    assert safe_input.command == "ifconfig"
    assert safe_input.args == ["-a"]
