# Log Storage and Retention

TraceNest manages log storage automatically with strict limits to ensure predictable disk usage and production safety.

All logs are stored locally and managed without manual intervention.

---

## Log Storage Location

By default, TraceNest stores logs inside the project root:

```text
TraceNestLogs/
```

This directory is created automatically when TraceNest is first used.

---

## Directory Structure

In day-wise mode (default), logs are stored as one file per day:

```text
TraceNestLogs/
├── 2026-01-10.log
├── 2026-01-11.log
├── 2026-01-12.log
└── archive/
```

The `archive/` directory is reserved for internal cleanup operations.

---

## Logging Modes

TraceNest supports two logging modes.

---

### Day-Wise Mode (Default)

In day-wise mode, TraceNest creates one log file per calendar day.

#### Behavior

- One log file per day
- Maximum size per day: **25–30 MB**
- Retention period: **60 days**
- Oldest log files are deleted automatically

#### Advantages

- Easy log navigation
- Predictable disk usage
- Suitable for long-running services
- Recommended for production systems

---

### Single-File Mode

In single-file mode, all logs are written to a single file.

```text
TraceNestLogs/current.log
```

#### Behavior

- Single log file
- Maximum size: **100 MB**
- Oldest log entries are removed first

#### Advantages

- Simple setup
- Suitable for small applications
- Useful during development

---

## Retention Policy

Retention rules are enforced automatically.

- Retention is based on file creation date
- Cleanup runs on application startup and during log writes
- No manual cleanup is required

Logs exceeding the configured retention period are permanently deleted.

---

## Size Enforcement

TraceNest enforces strict size limits to prevent disk exhaustion.

- Day-wise files are capped per day
- Single-file mode uses FIFO trimming
- Size checks are performed continuously

Applications never exceed configured disk limits.

---

## Cleanup Strategy

Cleanup follows these rules:

1. Oldest logs are deleted first
2. Active log files are never corrupted
3. Cleanup never blocks application execution
4. Failures are handled gracefully

---

## Configuration Interaction

Storage and retention behavior can be customized using the configuration file:

```text
TraceNestLogs/config.json
```

Relevant configuration options include:

- `mode`
- `retention_days`
- `max_size_mb`
- `single_file_max_size_mb`

---

## Best Practices

- Use day-wise mode for production workloads
- Monitor disk usage when increasing retention
- Avoid disabling retention limits
- Keep default limits unless necessary

---

## Safety Guarantees

TraceNest guarantees:

- No uncontrolled disk growth
- No blocking I/O operations
- No application crashes due to logging
- Safe operation in containers and servers

Log storage and retention are designed to be automatic, predictable, and production-safe.
