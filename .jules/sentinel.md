## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-24 - Argument Injection in Whitelisted Commands
**Vulnerability:** The `safe_command` tool whitelisted commands like `dig` and `ping` but failed to validate arguments, allowing attackers to perform file reads (`dig -f`), DoS attacks (`ping -f`), or other destructive actions via flag injection.
**Learning:** Whitelisting commands is insufficient if arguments are passed through blindly. "Safe" commands often have "unsafe" flags (e.g., file I/O, network manipulation) that can be exploited.
**Prevention:** Implement strict argument validation or an `ARGUMENT_BLOCKLIST` for whitelisted commands. Ensure validation logic accounts for combined flags (e.g., `-cf` contains `-f`) and prefix matching to prevent bypasses.
