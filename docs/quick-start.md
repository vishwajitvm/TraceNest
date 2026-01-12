# Quick Start

This guide helps you start using TraceNest in under two minutes.

TraceNest is designed to work immediately after installation with no configuration required.

---

## Step 1: Install TraceNest

Install TraceNest using pip:

```bash
pip install tracenest
```

---

## Step 2: Import the Logger

Import the TraceNest logger in your application:

```python
from tracenest import logger
```

No setup or initialization is required.

---

## Step 3: Write Your First Log

Start logging immediately:

```python
logger.info("Application started")
logger.error("Something went wrong", reason="example")
```

---

## What Happens Automatically

As soon as the logger is used, TraceNest:

- Creates a `TraceNestLogs/` directory in the project root
- Starts writing logs immediately
- Applies log rotation and retention rules
- Formats logs with timestamps and metadata
- Prepares the built-in UI (FastAPI projects)

No configuration files are needed.

---

## Log Output Location

Logs are written locally to:

```text
TraceNestLogs/
```

Inside this folder, logs are organized automatically based on the configured mode.

---

## Default Logging Mode

By default, TraceNest uses **day-wise logging**.

```text
TraceNestLogs/
├── 2026-01-12.log
├── 2026-01-13.log
└── archive/
```

### Default Limits

- One log file per day
- Maximum 25–30 MB per day
- Retention up to 60 days
- Old logs deleted automatically

---

## Using TraceNest with FastAPI

If you are using FastAPI, you can enable automatic request logging.

```python
from fastapi import FastAPI
from tracenest.fastapi import TraceNestMiddleware

app = FastAPI()
app.add_middleware(TraceNestMiddleware)
```

This automatically logs:
- Incoming requests
- Response status codes
- Execution time
- Unhandled exceptions

---

## Viewing Logs in the UI

When running a FastAPI application, access the TraceNest UI at:

```text
http://localhost:8001/tracenest
```

The UI allows you to:
- View logs in real time
- Filter and search logs
- Navigate by date
- Switch themes

---

## Next Steps

After completing the quick start, you may want to explore:

- Logging guidelines
- Configuration options
- Storage and retention behavior
- UI features
- FastAPI integration details

TraceNest is now fully set up and ready to use.
