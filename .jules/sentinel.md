## 2025-01-05 - [Command Injection via Argument Passing]
**Vulnerability:** The `safe_command` tool whitelisted command names (like `ip`) but allowed arbitrary arguments, enabling users to execute state-modifying subcommands (e.g., `ip addr add`) or disrupt services (`ifconfig eth0 down`).
**Learning:** Whitelisting command binaries is insufficient when the binary itself supports complex subcommands or dangerous flags. Tools must validate *all* input components, including arguments.
**Prevention:** Implement strict argument validation for sensitive CLI tools. Use whitelists for allowed subcommands where possible, or robust blacklists for known dangerous verbs/flags if a whitelist is too restrictive. Ensure argument parsing handles case sensitivity and batch modes.
