## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-21 - Dangerous Argument Injection in Safe Commands
**Vulnerability:** The `safe_command` tool whitelisted commands like `ping` and `dig` but did not validate arguments, allowing users to execute DoS attacks (`ping -f`) or read arbitrary files (`dig -f`).
**Learning:** Whitelisting commands is insufficient if arguments can change the command's behavior to be dangerous or destructive. Standard tools often have "dual-use" flags (e.g., debugging, batch processing) that can be abused.
**Prevention:** Implement an `ARGUMENT_BLOCKLIST` alongside command whitelists. Validate arguments against this blocklist, checking for both exact matches and combined flags (e.g., `-cf` containing `-f`).
