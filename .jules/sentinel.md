## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-02-07 - Safe Command Argument Injection
**Vulnerability:** The `troubleshooting_execute_safe_command` tool whitelisted `dig`, but failed to validate arguments. This allowed `dig -f /etc/passwd` to read arbitrary files.
**Learning:** Whitelisting commands is insufficient if arguments are not also validated. Many "safe" commands have dangerous flags (e.g., `-f` for file read/write, `-e` for execution).
**Prevention:** Implement `ARGUMENT_BLOCKLIST` for whitelisted commands to explicitly forbid dangerous flags. Validate arguments against this blocklist in the input model.
