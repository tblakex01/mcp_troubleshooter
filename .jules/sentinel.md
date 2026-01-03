## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-02-14 - Dangerous Arguments in Safe Commands
**Vulnerability:** Safe commands like `dig` or `ss` were whitelisted but their arguments were not validated, allowing attackers to use flags like `-f` (read file) or `-K` (kill socket) to bypass security restrictions.
**Learning:** Whitelisting commands is insufficient if the command itself has dangerous flags. Tools often have "dual use" features that can be exploited.
**Prevention:** Implement `ARGUMENT_BLOCKLIST` to explicitly reject dangerous flags for otherwise safe commands. Always assume CLI tools have powerful, potentially dangerous features that need to be restricted.
