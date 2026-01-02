## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-21 - Dangerous Argument Injection in Whitelisted Commands
**Vulnerability:** The `safe_command` tool whitelisted base commands (e.g., `dig`, `ip`) but failed to validate their arguments. Attackers could pass flags like `-f` to `dig` (arbitrary file read) or subcommands like `netns exec` to `ip` (arbitrary command execution).
**Learning:** Allow-listing binary names is insufficient security for "Swiss Army knife" tools like `ip` or `dig` that have destructive or privileged modes. The entire command line must be validated, not just the executable.
**Prevention:** Implement a secondary "Argument Blocklist" or strict "Argument Allowlist" for complex CLI tools. Sanitize inputs to prevent flag injection (e.g., `-f`) and block dangerous subcommands.
