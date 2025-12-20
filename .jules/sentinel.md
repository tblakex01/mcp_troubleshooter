## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.
## 2025-01-20 - Unsafe Diagnostic Command Execution
**Vulnerability:** The `safe_command` tool allowed dangerous arguments for state-changing commands like `ip` and `ifconfig` (e.g., `ip link set eth0 down`), enabling potential denial of service or network reconfiguration.
**Learning:** Whitelisting command names alone is insufficient for security; argument validation is crucial for tools that can modify system state. "Safe" commands often have "unsafe" modes.
**Prevention:** Implement strict argument filtering or dedicated wrapper functions for sensitive system commands. Blocklists for known dangerous keywords (like `set`, `add`, `delete`, `down`) provide an effective defense-in-depth layer when full grammar parsing is not feasible.
