# Troubleshooting MCP Server - Usage Examples

This document provides detailed, real-world examples for each tool in the Troubleshooting MCP Server.

## Table of Contents
1. [System Information Examples](#system-information-examples)
2. [Resource Monitoring Examples](#resource-monitoring-examples)
3. [Log File Analysis Examples](#log-file-analysis-examples)
4. [Network Diagnostics Examples](#network-diagnostics-examples)
5. [Process Management Examples](#process-management-examples)
6. [Environment Analysis Examples](#environment-analysis-examples)
7. [Safe Command Execution Examples](#safe-command-execution-examples)
8. [Multi-Tool Workflows](#multi-tool-workflows)

---

## System Information Examples

### Example 1: Quick System Overview
**User Query:**
```
"What kind of system am I running on?"
```

**Tool Response (Markdown):**
Shows operating system, hardware specs, Python version, CPU details, and memory/disk capacity.

**Use Case:** Initial system assessment, documentation, or support tickets.

---

### Example 2: Detailed Hardware Specs for Planning
**User Query:**
```
"Give me the system specifications in JSON format for my infrastructure documentation"
```

**Parameters:**
```json
{
  "response_format": "json"
}
```

**Use Case:** Automation, infrastructure as code, capacity planning.

---

## Resource Monitoring Examples

### Example 1: Check if System is Under Load
**User Query:**
```
"Is the system experiencing high CPU or memory usage?"
```

**Tool Response:**
Displays current CPU percentage, memory usage, and identifies if thresholds are concerning.

**Use Case:** Performance troubleshooting, capacity planning.

---

### Example 2: Detailed Per-Core Analysis
**User Query:**
```
"Show me CPU usage for each core separately"
```

**Parameters:**
```json
{
  "include_per_cpu": true,
  "response_format": "markdown"
}
```

**Use Case:** Identifying CPU bottlenecks, debugging multi-threaded applications.

---

### Example 3: Monitoring Before Deployment
**User Query:**
```
"Give me a baseline of current resource usage before I deploy the new service"
```

**Tool Response:**
Snapshot of CPU, memory, disk I/O, and network I/O that can be compared post-deployment.

**Use Case:** Change management, deployment validation.

---

## Log File Analysis Examples

### Example 1: Find Available Logs
**User Query:**
```
"What log files can I check on this system?"
```

**Parameters:**
```json
{
  "file_path": null
}
```

**Tool Response:**
Lists common log locations with size, last modified time, and read permissions.

**Use Case:** Initial troubleshooting, discovering relevant logs.

---

### Example 2: Check Recent System Errors
**User Query:**
```
"Show me the last 100 lines of the system log"
```

**Parameters:**
```json
{
  "file_path": "/var/log/syslog",
  "lines": 100
}
```

**Use Case:** General system troubleshooting, identifying recent issues.

---

### Example 3: Search for Authentication Failures
**User Query:**
```
"Find all 'Failed password' entries in auth.log from the last 200 lines"
```

**Parameters:**
```json
{
  "file_path": "/var/log/auth.log",
  "lines": 200,
  "search_pattern": "Failed password"
}
```

**Use Case:** Security auditing, investigating unauthorized access attempts.

---

### Example 4: Debug Application Errors
**User Query:**
```
"Search nginx error log for 500 errors in the last 500 lines"
```

**Parameters:**
```json
{
  "file_path": "/var/log/nginx/error.log",
  "lines": 500,
  "search_pattern": "500"
}
```

**Use Case:** Application debugging, troubleshooting production issues.

---

### Example 5: Monitor Database Issues
**User Query:**
```
"Check MySQL error log for 'connection' issues"
```

**Parameters:**
```json
{
  "file_path": "/var/log/mysql/error.log",
  "lines": 300,
  "search_pattern": "connection"
}
```

**Use Case:** Database performance troubleshooting, connection pool issues.

---

## Network Diagnostics Examples

### Example 1: Test Internet Connectivity
**User Query:**
```
"Can this server reach the internet? Test google.com"
```

**Parameters:**
```json
{
  "host": "google.com",
  "timeout": 5
}
```

**Tool Response:**
- DNS resolution status and IP
- Reachability confirmation

**Use Case:** Network troubleshooting, firewall validation.

---

### Example 2: Verify Web Service Availability
**User Query:**
```
"Is my web application responding? Check example.com on port 443"
```

**Parameters:**
```json
{
  "host": "example.com",
  "port": 443,
  "timeout": 10
}
```

**Tool Response:**
- DNS resolution
- Port 443 connectivity status
- Connection timing

**Use Case:** Service availability checks, SSL/TLS endpoint testing.

---

### Example 3: Test Database Connectivity
**User Query:**
```
"Can I connect to the PostgreSQL database at db.example.com port 5432?"
```

**Parameters:**
```json
{
  "host": "db.example.com",
  "port": 5432,
  "timeout": 5
}
```

**Use Case:** Database connection troubleshooting, network segmentation testing.

---

### Example 4: Check SSH Access
**User Query:**
```
"Verify SSH is accessible on production-server.example.com"
```

**Parameters:**
```json
{
  "host": "production-server.example.com",
  "port": 22,
  "timeout": 10
}
```

**Use Case:** Remote access verification, security testing.

---

### Example 5: Test Internal Service
**User Query:**
```
"Test if the Redis cache at 10.0.1.50 port 6379 is reachable"
```

**Parameters:**
```json
{
  "host": "10.0.1.50",
  "port": 6379,
  "timeout": 5
}
```

**Use Case:** Microservice connectivity, internal service mesh testing.

---

## Process Management Examples

### Example 1: Check if Service is Running
**User Query:**
```
"Is nginx running on this server?"
```

**Parameters:**
```json
{
  "pattern": "nginx",
  "limit": 20
}
```

**Tool Response:**
Lists all nginx processes with CPU/memory usage, PIDs, and status.

**Use Case:** Service health checks, deployment verification.

---

### Example 2: Find Resource-Heavy Processes
**User Query:**
```
"What processes are using the most resources?"
```

**Parameters:**
```json
{
  "pattern": null,
  "limit": 10,
  "response_format": "markdown"
}
```

**Tool Response:**
Top 10 processes sorted by CPU usage.

**Use Case:** Performance troubleshooting, identifying resource hogs.

---

### Example 3: Debug Application Issues
**User Query:**
```
"Show me all Python processes and their memory usage"
```

**Parameters:**
```json
{
  "pattern": "python",
  "limit": 20,
  "response_format": "json"
}
```

**Use Case:** Application debugging, memory leak investigation.

---

### Example 4: Check Docker Containers
**User Query:**
```
"List all Docker-related processes"
```

**Parameters:**
```json
{
  "pattern": "docker",
  "limit": 50
}
```

**Use Case:** Container troubleshooting, orchestration debugging.

---

## Environment Analysis Examples

### Example 1: Check Development Environment
**User Query:**
```
"What development tools are installed and their versions?"
```

**Parameters:**
```json
{
  "pattern": null,
  "response_format": "markdown"
}
```

**Tool Response:**
Lists installed tools (Python, Node, Git, Docker, etc.) with versions.

**Use Case:** Environment setup validation, onboarding new developers.

---

### Example 2: Debug PATH Issues
**User Query:**
```
"Show me all PATH-related environment variables"
```

**Parameters:**
```json
{
  "pattern": "PATH",
  "response_format": "markdown"
}
```

**Use Case:** Command not found errors, binary resolution issues.

---

### Example 3: Check AWS Configuration
**User Query:**
```
"List all AWS-related environment variables"
```

**Parameters:**
```json
{
  "pattern": "AWS",
  "response_format": "json"
}
```

**Use Case:** Cloud provider configuration, credential troubleshooting.

---

### Example 4: Verify CI/CD Environment
**User Query:**
```
"Show me all environment variables containing 'CI' or 'BUILD'"
```

**Parameters:**
```json
{
  "pattern": "CI",
  "response_format": "markdown"
}
```

**Use Case:** CI/CD pipeline debugging, build environment issues.

---

## Safe Command Execution Examples

### Example 1: Check Disk Space
**User Query:**
```
"Show disk usage in human-readable format"
```

**Parameters:**
```json
{
  "command": "df",
  "args": ["-h"],
  "timeout": 30
}
```

**Tool Response:**
Disk usage for all mounted filesystems.

**Use Case:** Capacity management, investigating disk full errors.

---

### Example 2: Test Network Connectivity
**User Query:**
```
"Ping google.com 5 times to test connectivity"
```

**Parameters:**
```json
{
  "command": "ping",
  "args": ["-c", "5", "google.com"],
  "timeout": 30
}
```

**Use Case:** Network troubleshooting, latency testing.

---

### Example 3: Check System Uptime
**User Query:**
```
"How long has the system been running?"
```

**Parameters:**
```json
{
  "command": "uptime",
  "args": [],
  "timeout": 5
}
```

**Use Case:** Stability assessment, maintenance window planning.

---

### Example 4: List Block Devices
**User Query:**
```
"Show me all block devices and their mount points"
```

**Parameters:**
```json
{
  "command": "lsblk",
  "args": [],
  "timeout": 10
}
```

**Use Case:** Storage troubleshooting, disk identification.

---

### Example 5: Check Network Connections
**User Query:**
```
"Show all listening TCP ports"
```

**Parameters:**
```json
{
  "command": "netstat",
  "args": ["-tuln"],
  "timeout": 15
}
```

**Use Case:** Security auditing, port conflict resolution.

---

## Multi-Tool Workflows

### Workflow 1: Complete System Health Check
**Scenario:** Investigate overall system health

**Steps:**
1. Get system info: "What are the system specifications?"
2. Check resources: "Show current CPU and memory usage"
3. Review logs: "Check system log for errors in last 100 lines"
4. Check processes: "What are the top 10 processes by CPU usage?"
5. Test connectivity: "Can the system reach the internet?"

---

### Workflow 2: Application Deployment Validation
**Scenario:** Verify successful application deployment

**Steps:**
1. Check process: "Is nginx running?"
2. Test endpoint: "Verify port 443 is accessible on app.example.com"
3. Review logs: "Check nginx error log for issues in last 200 lines"
4. Monitor resources: "Show resource usage to establish baseline"

---

### Workflow 3: Security Incident Investigation
**Scenario:** Investigate potential security breach

**Steps:**
1. Check auth logs: "Find 'Failed password' in auth.log last 500 lines"
2. Review connections: "Run 'netstat -tuln' to see active connections"
3. Check processes: "List all processes for suspicious activity"
4. Test external access: "Verify external services are accessible"

---

### Workflow 4: Performance Troubleshooting
**Scenario:** System running slowly

**Steps:**
1. Check resources: "Show CPU and memory usage with per-core details"
2. Find heavy processes: "What processes use the most resources?"
3. Check disk I/O: "Monitor disk I/O statistics"
4. Review system logs: "Search system log for 'error' or 'warning'"
5. Verify disk space: "Run 'df -h' to check available disk space"

---

### Workflow 5: Environment Setup Validation
**Scenario:** New developer onboarding

**Steps:**
1. Check system: "What operating system and hardware?"
2. Verify tools: "What development tools are installed?"
3. Check environment: "Show all PATH-related variables"
4. Test connectivity: "Can I reach github.com?"
5. Verify services: "Are Docker and Git properly configured?"

---

## Tips for Effective Use

### 1. Combining Filters for Focused Results
Instead of retrieving all data, use filters:
- **Processes:** Search by pattern instead of listing all
- **Logs:** Use search_pattern to find specific issues
- **Environment:** Filter by pattern to find related variables

### 2. Progressive Investigation
Start broad, then narrow down:
1. Get system overview
2. Identify problem areas
3. Deep dive with specific queries
4. Use multiple tools together

### 3. Using JSON for Automation
When building scripts or automation:
- Use `response_format="json"` for structured data
- Parse the JSON response programmatically
- Chain multiple tool calls together

### 4. Respecting Character Limits
For large datasets:
- Use pattern filters to reduce results
- Limit log line counts appropriately
- Request smaller batches of data

### 5. Timeout Configuration
Adjust timeouts based on operation:
- Quick checks: 5-10 seconds
- Network operations: 10-30 seconds
- Command execution: 30-60 seconds for safe commands

---

## Common Troubleshooting Patterns

### Pattern 1: "Service Not Responding"
1. Check if process is running (search_processes)
2. Test port connectivity (test_network_connectivity)
3. Review service logs (read_log_file)
4. Check resource usage (monitor_resources)

### Pattern 2: "High Memory Usage"
1. Get resource snapshot (monitor_resources)
2. Find memory-heavy processes (search_processes)
3. Check for memory leaks in logs (read_log_file)
4. Verify system specs (get_system_info)

### Pattern 3: "Connection Failures"
1. Test basic connectivity (test_network_connectivity)
2. Check DNS resolution
3. Verify firewall rules (execute_safe_command with netstat)
4. Review network configuration (inspect_environment)

### Pattern 4: "Deployment Issues"
1. Verify service started (search_processes)
2. Check application logs (read_log_file)
3. Test endpoints (test_network_connectivity)
4. Verify environment (inspect_environment)

---

## Best Practices

1. **Always start with system info** to understand the context
2. **Use pattern filters** to get focused results
3. **Combine multiple tools** for comprehensive diagnostics
4. **Check logs** when investigating issues
5. **Test connectivity** before assuming network problems
6. **Monitor resources** to identify bottlenecks
7. **Document findings** using JSON format for records
8. **Respect timeouts** and adjust as needed
9. **Start broad, then narrow** your investigation
10. **Use markdown for humans, JSON for machines**

---

For more information, see the main [README.md](README.md) documentation.
