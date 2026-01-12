# Configuration

TraceNest is designed to work out of the box with **zero configuration**.
For most projects, no configuration file is required.

Configuration is **optional** and intended only for advanced use cases.

---

## Configuration File Location

When configuration is required, TraceNest reads from the following location:

```text
TraceNestLogs/config.json
```

This file is created automatically only when custom configuration is needed.

---

## Default Configuration

If no configuration file is present, TraceNest uses the following defaults:

```json
{
  "mode": "day-wise",
  "retention_days": 60,
  "max_size_mb": 30,
  "single_file_max_size_mb": 100,
  "ui_enabled": true,
  "log_level": "info"
}
```

---

## Configuration Options

### mode

Defines how logs are stored.

Allowed values:
- `day-wise` (default)
- `single-file`

```json
{
  "mode": "day-wise"
}
```

---

### retention_days

Specifies how many days logs are retained in **day-wise mode**.

- Default: `60`
- Minimum: `1`

```json
{
  "retention_days": 60
}
```

Logs older than the specified number of days are deleted automatically.

---

### max_size_mb

Defines the maximum allowed size **per day** in day-wise mode.

- Default: `30`
- Recommended range: `25–30`

```json
{
  "max_size_mb": 30
}
```

Once the limit is reached, older logs for that day are trimmed automatically.

---

### single_file_max_size_mb

Defines the maximum size of the log file in **single-file mode**.

- Default: `100`

```json
{
  "single_file_max_size_mb": 100
}
```

When the size limit is exceeded, the oldest log entries are removed first.

---

### ui_enabled

Enables or disables the built-in TraceNest UI.

- Default: `true`

```json
{
  "ui_enabled": true
}
```

When disabled, the `/tracenest` route is not exposed.

---

### log_level

Defines the minimum log level to be recorded.

Allowed values:
- `debug`
- `info`
- `warn`
- `error`
- `critical`
- `audit`
- `security`

```json
{
  "log_level": "info"
}
```

Logs below the specified level are ignored.

---

## Example Custom Configuration

```json
{
  "mode": "day-wise",
  "retention_days": 30,
  "max_size_mb": 25,
  "ui_enabled": true,
  "log_level": "info"
}
```

---

## Configuration Loading Behavior

- Configuration is loaded at application startup
- Changes require an application restart
- Invalid values fall back to defaults
- Configuration errors never crash the application

---

## Best Practices

- Use default configuration whenever possible
- Avoid increasing retention without monitoring disk usage
- Disable the UI in production if not required
- Prefer day-wise mode for long-running services

---

## Safety Guarantees

- Configuration errors are handled gracefully
- No configuration option can block application execution
- Disk usage is always bounded by configured limits

TraceNest configuration is intentionally simple, predictable, and safe.
