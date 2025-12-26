## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-20 - Command Injection via Safe Command Tool
**Vulnerability:** The `safe_command` tool whitelisted command names (e.g., `ip`, `dig`) but failed to validate arguments. This allowed attackers to use flags like `ip -batch` or `ip netns exec` to execute arbitrary commands or read sensitive files.
**Learning:** Whitelisting binaries is insufficient for security; many standard utilities have "dual-use" flags that can turn them into execution primitives.
**Prevention:** Implement strict argument validation using Pydantic validators. Block known dangerous flags (e.g., `-batch`, `-exec`, `-f`) and restrict complex tools like `ip` to a specific set of safe subcommands.
