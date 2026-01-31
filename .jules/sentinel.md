## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-21 - Dangerous Argument Injection in Safe Commands
**Vulnerability:** The `safe_command` tool whitelisted commands like `ping` and `lsof` but failed to validate their arguments, allowing dangerous flags (e.g., `ping -f` for flood attacks, `lsof -b`).
**Learning:** Whitelisting command names is insufficient for security; many "safe" tools have flags that can turn them into denial-of-service vectors or privacy leaks.
**Prevention:** Implement a strict argument blocklist (or allowlist) for each command. Added validation in `SafeCommandInput` to reject arguments starting with known dangerous flags defined in `ARGUMENT_BLOCKLIST`.
