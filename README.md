# TraceNest

TraceNest is a **developer-first, local-first logging SDK for Python applications** designed to remove the operational burden of log management from developers.

You focus on building features.  
TraceNest takes care of logging.

---

## What is TraceNest?

TraceNest is not just a logger.  
It is a **logging infrastructure layer** embedded directly into your application.

It automatically:
- Creates and manages log files
- Rotates logs safely
- Enforces retention limits
- Provides a built-in UI to view logs
- Integrates seamlessly with FastAPI
- Works out of the box with zero configuration

---

## Why TraceNest Exists

Traditional logging requires developers to:
- Configure log handlers
- Manage file rotation
- Clean up old logs
- Build tools to inspect logs

TraceNest eliminates this complexity by handling **the entire log lifecycle automatically**.

---

## Key Features

- Zero-configuration setup
- Automatic `TraceNestLogs/` folder creation
- Day-wise or single-file logging modes
- Strict size and retention enforcement
- Built-in UI served from the application
- Structured, metadata-rich logs
- Native FastAPI middleware
- Safe, non-blocking design
- Free and easy to integrate

---

## Installation

```bash
pip install tracenest
```

---

## Quick Usage

```python
from tracenest import logger

logger.info("Application started")
logger.error("Payment failed", order_id=123)
```

Logs are immediately written to:

```text
TraceNestLogs/
```

No configuration required.

---

## Log Storage

By default, TraceNest stores logs locally inside the project root:

```text
TraceNestLogs/
├── 2026-01-10.log
├── 2026-01-11.log
└── archive/
```

### Default Behavior

- One log file per day
- Maximum 25–30 MB per day
- Retention up to 60 days
- Old logs deleted automatically

A single-file mode is also available for smaller projects.

---

## Built-In UI

When used with FastAPI, TraceNest exposes a local UI automatically:

```text
http://localhost:8000/tracenest
```

### UI Features

- Live log streaming
- Search and filtering
- Date-based navigation
- Download logs
- Clear logs
- Theme selection

### Available Themes

- Light
- Dark
- Blue-Dark

---

## FastAPI Integration

TraceNest provides native FastAPI middleware for automatic request logging.

```python
from tracenest.fastapi import TraceNestMiddleware

app.add_middleware(TraceNestMiddleware)
```

Automatically logs:
- Incoming requests
- Response status codes
- Request duration
- Unhandled exceptions

---

## Safety and Performance

TraceNest is designed to be production-safe.

- Never blocks application execution
- Uses buffered I/O
- Minimal memory footprint
- Graceful fallback on failure
- Works inside Docker and containers

TraceNest will **never crash your application**.

---

## Changelog

### v0.1.7 - 2026-07-03
* Markdown-based changelog system directly integrated into the UI.
* Dynamic Versions modal featuring a beautiful two-pane layout, fetching and rendering markdown using `marked.js`.
* Synced main project `README.md` with the full project changelog to ensure release notes are visible directly on PyPI.
* Improved UI links, adding proper developer attribution linking back to GitHub in the UI footer.
* Removed the static `changelog.json` in favor of the dynamic API.

### v0.1.6 - 2026-07-03
* Added built-in secret redaction to prevent credentials, tokens, API keys, cookies, and database passwords from leaking in logs.
* Added recursive masking for dictionaries, lists, nested metadata, request data, and response data.
* Added pattern-based masking for raw log strings, Authorization headers, JWTs, database URLs, Redis URLs, and key-value secrets.
* Logs are now redacted before storage and before UI/API display for defense-in-depth safety.
* Middleware logging now masks sensitive headers, cookies, request bodies, and response bodies.
* Added tests for key-based redaction, regex redaction, nested data structures, middleware safety, and custom redaction configuration.

### v0.1.5 - 2026-07-03
* Latest logs are now shown first by default (reverse chronological order).
* Added beautiful UI badges for log levels to improve readability.
* Timestamps converted to readable relative times (e.g. '2 minutes ago') with exact time on hover.
* Enhanced overall UI aesthetics with animations, shadow effects, and a premium feel.

### Version 0.1.4 - 2026-07-02
* Initial stable release with dynamic UI and real-time log tailing.
* Search, filter, and pagination capabilities added.

### Version 0.1.3 - 2026-07-01
* **Fixed UI Delay Issue:** Implemented a background flush thread that automatically syncs buffered logs to the disk every 1 second, completely resolving the 2-10 minute UI delay on low-traffic applications.
* **Auto-Refreshing UI:** The web UI now features automatic polling, instantly displaying new logs as soon as they are written without requiring manual page reloads.

---

## Documentation

Detailed documentation is available in the `docs/` folder:

- Introduction & philosophy
- Quick start
- Logging guidelines
- Configuration
- Storage & retention
- UI usage
- FastAPI integration
- Performance guarantees
- Version history

---

## Versioning

TraceNest follows semantic versioning.

### Current Version: `0.1.7`

Includes:
- Core logging API
- Automatic folder creation
- Day-wise and single-file logging
- Retention enforcement
- Built-in UI
- FastAPI middleware

---

## Philosophy

TraceNest is built on three principles:

1. Zero friction for developers  
2. Full transparency of logs  
3. Production-grade safety by default  

---

## Author & Maintainer

**VishwajitVM**

- 📍 New Delhi, India  
- 🐙 GitHub: https://github.com/vishwajitvm  
- ✉️ Email: vishwajitmall50@gmail.com  

TraceNest is actively maintained with a strong focus on real-world production use cases, developer experience, and long-term scalability.

---

## License

TraceNest SDK is free to use and distributed under an open-source license.
