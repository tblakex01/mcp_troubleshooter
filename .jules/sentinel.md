## 2024-05-23 - Path Traversal in Log Reader
**Vulnerability:** The `troubleshooting_read_log_file` tool allowed arbitrary file reading because it validated that the path existed and was a file, but did not restrict *where* the file was located. A user could read `/etc/passwd` or any other file readable by the process.
**Learning:** `Path.resolve()` is crucial for canonicalizing paths to prevent traversal attacks (like `../`), but it must be combined with a check like `is_relative_to()` against a whitelist of allowed directories. Validating "is it a file" is insufficient for security.
**Prevention:** Always define a security boundary (whitelist of allowed directories) for file access tools and enforce it using canonical paths.
