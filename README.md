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

### Current Version: `0.1.0`

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
