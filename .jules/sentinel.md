## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2026-02-14 - Argument Injection in Whitelisted Commands
**Vulnerability:** Whitelisted diagnostic commands like `dig`, `ip`, and `ss` were allowed to execute with arbitrary arguments. Attackers could inject flags like `dig -f` (file read), `ip -b` (command execution via file), or `ss -D` (file overwrite) to bypass restrictions and access/modify the filesystem.
**Learning:** Whitelisting commands is insufficient if arguments are not also validated. Many "safe" commands have obscure flags that can be abused for file operations or execution control.
**Prevention:** Implement a strict argument validator or blocklist for each whitelisted command. Validate all arguments against known dangerous patterns (e.g., `-f` for `dig`, `-b` for `ip`) and ensure no unvalidated input is passed to shell commands.
