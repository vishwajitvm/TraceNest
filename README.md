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

### v0.1.14 - 2026-07-16
* Fixed a Mermaid syntax error in the documentation (`01_introduction.md`) that caused the high-level architecture diagram to fail to render on GitHub.

### v0.1.13 - 2026-07-16
* Completely rebuilt the `docs/` folder with an exhaustive, beginner-friendly 14-chapter Master Guide! Everything from core concepts (Configuration, Formatter, Retention, Rotation) to Advanced Customizations and Troubleshooting is now thoroughly explained with examples and diagrams.

### v0.1.12 - 2026-07-15
* Fixed z-index issue causing the dropdown menus (Levels and Themes) to incorrectly render underneath the sticky table headers.

### v0.1.11 - 2026-07-15
* 4 Beautiful New Themes: Emerald (Green), Ruby (Red), Amethyst (Purple), and Midnight (OLED High Contrast).
* Redesigned footer showcasing the current TraceNest version and developer credit.
* Fixed search input box retaining a white background when using dark themes.

### v0.1.10 - 2026-07-15
* Fixed white background issue on table rows and dropdown menus when using Dark or Dark Blue themes. All components now properly inherit theme colors.

### v0.1.9 - 2026-07-15
* Fatal UI crash preventing logs from displaying on fresh installs due to a DOM mismatch.
* Replaced inline level badges with a clean dropdown menu for improved UX.
* Removed the "Versions" modal entirely for a simpler, decluttered interface.

### v0.1.8 - 2026-07-15
* Auto-refresh functionality to stream logs live in the dashboard without manually reloading.
* Manual refresh button.
* Slide-out Details Panel providing deep-dive capabilities into structured logs and traceback without losing table context.
* PyPI version checking directly in the UI versions modal.
* Completely redesigned UI dashboard inspired by modern observability platforms (e.g., Grafana/Vercel).
* High contrast, beautiful themes (Dark, Light, Dark Blue) relying on modern `CSS variables`.
* Achieved O(1) table updates per polling interval by intelligently caching parsed logs and dynamically computing diffs on the frontend.
* Current log selection bug: Re-rendering the dashboard on polling no longer destroys user selection.

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

### Current Version: `0.1.14`

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
