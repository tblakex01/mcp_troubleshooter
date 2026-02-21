## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-21 - Command Argument Injection in Safe Tools
**Vulnerability:** The `safe_command` tool whitelisted command binaries but allowed arbitrary arguments, enabling abuse (e.g., `ip netns exec` for RCE, `ping -f` for DoS).
**Learning:** Whitelisting binaries is insufficient for security if the binary supports flags that allow command execution, file system access, or resource exhaustion. Tools like `ip`, `find`, or `awk` are dual-use and can be weaponized via arguments.
**Prevention:** Implement strict argument validation (allowlist preferred, or robust blocklist) alongside binary whitelisting. For complex tools like `ip`, block specific subcommands or flags known to be dangerous.
