## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-20 - RCE in 'safe_command' Tool via Argument Injection
**Vulnerability:** The `safe_command` tool allowed arbitrary arguments for the `ip` command. This permitted RCE via `ip netns exec <command>` and file reading via `ip -batch <file>`.
**Learning:** Whitelisting command names is insufficient if the command itself has "unsafe" subcommands or flags (like `-exec`, `-batch`, `-script`).
**Prevention:** For complex commands like `ip` or `dig`, we must also validate arguments against a blocklist of dangerous flags/subcommands or, ideally, a whitelist of allowed patterns.
