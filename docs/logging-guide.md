# Logging Guide

This guide explains how to use TraceNest logging effectively and consistently across your application.

TraceNest follows structured, level-based logging designed for production environments.

---

## Logging Basics

To start logging, import the TraceNest logger:

```python
from tracenest import logger
```

You can then log messages using predefined log levels.

---

## Log Levels

TraceNest supports the following log levels:

| Level | Purpose |
|------|--------|
| debug | Development and diagnostic information |
| info | Normal application flow |
| warn | Non-critical issues |
| error | Recoverable failures |
| critical | System-level failures |
| audit | Compliance and audit events |
| security | Security-related events |

---

## Basic Logging

```python
logger.info("Application started")
```

This records a simple informational message.

---

## Structured Logging

TraceNest encourages structured logging using key-value metadata.

```python
logger.error(
    "Payment failed",
    user_id=123,
    order_id=456,
    amount=500
)
```

Structured data improves readability, filtering, and debugging.

---

## Debug Logging

Use debug logs for development and troubleshooting.

```python
logger.debug("Fetching user profile", user_id=42)
```

Debug logs can be filtered using configuration.

---

## Warning Logs

Use warnings for unexpected but non-fatal situations.

```python
logger.warn("Cache miss occurred", key="user_42")
```

---

## Error Logs

Error logs indicate failures that were handled by the application.

```python
logger.error("Database connection timeout", db="users")
```

Error logs may include stack traces when available.

---

## Critical Logs

Critical logs represent severe failures that may require immediate attention.

```python
logger.critical("Service unavailable")
```

Use this level sparingly.

---

## Audit Logs

Audit logs are intended for compliance-related events.

```python
logger.audit("User role changed", admin_id=1, user_id=42)
```

Audit logs are immutable by design.

---

## Security Logs

Security logs capture authentication, authorization, and security events.

```python
logger.security("Invalid login attempt", ip="192.168.1.10")
```

Security logs should never include sensitive data.

---

## Log Message Guidelines

- Keep messages concise and meaningful
- Avoid logging secrets or credentials
- Use metadata instead of string concatenation
- Be consistent with log levels

---

## File and Line Context

TraceNest automatically captures:

- Source file name
- Line number
- Timestamp (UTC)
- Thread or async context

No manual configuration is required.

---

## Viewing Logs

Logs can be viewed:

- Directly from files in `TraceNestLogs/`
- Through the built-in TraceNest UI

---

## Performance Considerations

- Logging is non-blocking
- Metadata is serialized efficiently
- Large objects should not be logged directly

---

## Best Practices

- Use `info` for business flow
- Use `debug` only during development
- Use `error` for recoverable issues
- Use `critical` for system failures
- Use `audit` and `security` consistently

Effective logging improves observability and long-term maintainability.
