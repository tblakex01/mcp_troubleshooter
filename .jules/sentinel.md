## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-20 - Indirect Command Execution via Diagnostic Tools
**Vulnerability:** The `ip` command was whitelisted for diagnostic purposes, but it allows executing arbitrary commands via `ip netns exec`. This bypassed the command whitelist entirely.
**Learning:** Whitelisting commands is insufficient if those commands have flags or subcommands that allow executing other programs. "Safe" tools often have "unsafe" features for power users.
**Prevention:** Whitelists must include argument validation, not just command names. Block specific dangerous arguments (like `exec`, `-exec`, `command`, etc.) for each allowed tool. Defense in depth: also block shell metacharacters in arguments.
