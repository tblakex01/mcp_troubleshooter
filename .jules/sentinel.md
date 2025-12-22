## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-22 - Argument Injection in Safe Command Execution
**Vulnerability:** The `safe_command` tool whitelisted command names (e.g., `ip`, `ifconfig`) but failed to validate arguments, allowing attackers to use subcommands like `ip link set` or `ifconfig down` to modify system state or cause denial of service.
**Learning:** Whitelisting binaries is insufficient when those binaries have "Swiss Army knife" capabilities. Security must be granular—validating not just *what* runs, but *how* it runs (arguments, flags).
**Prevention:** Implement deep argument inspection for sensitive tools. Define "safe" usage patterns (e.g., `ip addr show` is safe, `ip addr add` is not) and strictly validate arguments against allowed patterns or block known dangerous keywords.
