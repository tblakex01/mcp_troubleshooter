## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-28 - Secondary Command Injection in `ip` Tool
**Vulnerability:** The `safe_command` tool whitelisted `ip`, but failed to block subcommands like `ip netns exec` which allow arbitrary code execution in a network namespace.
**Learning:** Binary whitelisting is insufficient for "swiss-army knife" tools (like `ip`, `find`, `awk`, `git`) that have built-in execution capabilities. Trusting the binary name assumes all its modes are safe, which is often false.
**Prevention:** When whitelisting powerful system tools, explicitly blacklist dangerous flags/subcommands or, better yet, whitelist only specific argument patterns. Always audit the full capability set of a binary before considering it "safe".
