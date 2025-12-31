## 2025-01-20 - Environment Variable Leaks in Diagnostic Tools
**Vulnerability:** The `environment_inspect` tool was returning all environment variables without filtering, potentially exposing sensitive credentials like `AWS_SECRET_ACCESS_KEY` or `DB_PASSWORD`.
**Learning:** Diagnostic tools that dump system state often overlook the sensitivity of the data they collect. "Observability" can easily become "Information Disclosure" if not scoped correctly.
**Prevention:** Implement a mandatory "masking layer" for any tool that retrieves environment variables or configuration settings. This layer should check keys against a blocklist of sensitive patterns (e.g., `*SECRET*`, `*KEY*`, `*PASSWORD*`) before returning the value.

## 2025-01-31 - Command Line Argument Leaks in Process Search
**Vulnerability:** The `process_search` tool returned full command line arguments for running processes, which often contain sensitive credentials (e.g., `java -Dpassword=...`, `mysql -p...`).
**Learning:** Process listings are a common source of information leakage. Developers often pass secrets as command line arguments, assuming they are ephemeral, but they are visible to anyone who can list processes.
**Prevention:** Implement a masking mechanism for command line arguments in any process listing tool. Use regex patterns to identify and mask values associated with sensitive keys like `password`, `secret`, `token`, etc.
