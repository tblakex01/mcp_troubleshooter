"""
Constants used throughout the Troubleshooting MCP Server.
"""

# Maximum response size in characters
CHARACTER_LIMIT = 25000

# Whitelisted safe commands that can be executed
SAFE_COMMANDS = {
    "ping",
    "traceroute",
    "nslookup",
    "dig",
    "netstat",
    "ss",
    "ip",
    "ifconfig",
    "df",
    "du",
    "free",
    "uptime",
    "uname",
    "lsblk",
    "lsof",
    "whoami",
    "hostname",
}

# Blocklist of dangerous arguments for specific commands to prevent exploitation
ARGUMENT_BLOCKLIST = {
    "dig": ["-f"],
    "ip": ["-b", "-batch"],
    "ss": ["-D", "--dump", "-F", "--filter"],
    "ping": ["-f", "-i"],
}

# Common log file locations across different systems
COMMON_LOG_PATHS = [
    # Linux system logs
    "/var/log/syslog",
    "/var/log/messages",
    "/var/log/kern.log",
    "/var/log/auth.log",
    # Application logs (Linux)
    "/var/log/apache2/error.log",
    "/var/log/nginx/error.log",
    "/var/log/mysql/error.log",
    # Windows event logs
    "C:/Windows/System32/winevt/Logs/System.evtx",
    "C:/Windows/System32/winevt/Logs/Application.evtx",
]

# Allowed directories for log reading (security restriction)
ALLOWED_LOG_DIRS = [
    "/var/log",
    "/var/adm",
    "/var/eventlog",
    "/usr/local/var/log",
    "C:/Windows/System32/winevt/Logs",
]

# Patterns for sensitive environment variables to mask (Regex)
SENSITIVE_ENV_PATTERNS = [
    r".*PASSWORD.*",
    r".*SECRET.*",
    r".*CREDENTIAL.*",
    r"(?:^|_)KEY$",
    r"(?:^|_)TOKEN$",
    r"(?:^|_)AUTH$",
    r"(?:^|_)CERT$",
    r"(?:^|_)PRIVATE$",
]
