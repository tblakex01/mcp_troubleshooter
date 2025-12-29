## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-29 - Command Injection via Allowed Binary Arguments
**Vulnerability:** The `safe_command` tool whitelisted the `ip` binary but did not validate its arguments. This allowed attackers to use `ip netns exec` to execute arbitrary commands, bypassing the whitelist.
**Learning:** Whitelisting binaries is insufficient if the binaries themselves have features that allow command execution or system modification (like `exec`, `write`, `mount`). "Safe" tools often have "unsafe" modes.
**Prevention:** Implement deep argument validation for whitelisted commands. For complex tools like `ip` or `find`, explicitly block dangerous flags (`-exec`, `netns`) or whitelist only specific safe subcommands (`ip addr show`).
