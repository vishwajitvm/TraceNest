# UI Guide

TraceNest includes a built-in, lightweight user interface that allows developers to view and inspect logs directly from their application.

The UI is designed to be simple, fast, and local-first.

---

## Accessing the UI

When TraceNest is used with FastAPI and the UI is enabled, it is automatically exposed at:

```text
http://localhost:8000/tracenest
```

No additional setup or configuration is required.

---

## Purpose of the UI

The TraceNest UI is intended for:

- Local development debugging
- Quick inspection of production logs
- Verifying application behavior
- Troubleshooting errors without external tools

It is not intended to replace enterprise log analysis platforms.

---

## UI Features

The built-in UI provides the following capabilities:

- Live log streaming (tail mode)
- Filter logs by level (info, error, debug, etc.)
- Search logs by keyword
- Navigate logs by date
- Download log files
- Clear log files (optional)

All operations are read-only by default unless explicitly configured otherwise.

---

## Log Views

### Live View

Displays logs in real time as they are written by the application.

This is useful for:
- Debugging active requests
- Monitoring startup behavior
- Observing errors as they occur

---

### Date-Based View

Allows selection of logs from a specific date when day-wise logging mode is enabled.

This is useful for:
- Investigating past incidents
- Reviewing historical behavior
- Auditing application events

---

## Theme Support

TraceNest UI supports multiple visual themes to suit developer preferences.

Available themes:

- Light
- Dark
- Blue-Dark

The selected theme is stored locally in the browser and persists across sessions.

---

## Performance Characteristics

- UI reads logs directly from local files
- No database or external service is used
- Rendering is optimized for large log files
- UI does not impact application performance

---

## Security Considerations

- UI is exposed only within the running application
- No authentication is enabled by default
- Logs are never sent externally
- Sensitive data should not be logged

For production environments, access to the UI route should be restricted at the network or application level if required.

---

## Enabling or Disabling the UI

The UI can be enabled or disabled using configuration.

```json
{
  "ui_enabled": true
}
```

When disabled, the `/tracenest` route is not exposed.

---

## Best Practices

- Use the UI primarily in development and staging
- Avoid exposing the UI publicly in production
- Combine UI usage with day-wise logging mode
- Do not log secrets or sensitive payloads

---

## Limitations

- UI is local-only
- No multi-user support
- No role-based access control
- No remote access

These limitations are intentional to keep the UI lightweight and safe.

---

## Design Philosophy

The TraceNest UI is designed to:

- Be instantly available
- Require zero setup
- Remain simple and predictable
- Never interfere with application behavior

It exists to make logs visible, not to add complexity.
