## 2026-01-05 - Safe Command Argument Injection
**Vulnerability:** The `troubleshooting_execute_safe_command` tool allowed arbitrary arguments to be passed to whitelisted commands. This enabled attackers to use `dig -f` to read arbitrary files from the system, or `ping -f` to flood the network.
**Learning:** Whitelisting commands is not enough; arguments must also be validated or sanitized, especially when the underlying command supports flags that can change its behavior drastically (e.g., from network probe to file reader).
**Prevention:** Implemented an `ARGUMENT_BLOCKLIST` in `constants.py` and a validator in `models.py` to reject dangerous arguments (exact matches or combined flags) for specific commands.
