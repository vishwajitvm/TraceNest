# TraceNest

TraceNest is a **developer-first, local-first logging SDK for Python applications** designed to remove the operational burden of log management from developers.

You focus on building features.  
TraceNest takes care of logging.

---

## 📖 What is TraceNest?

TraceNest is not just a logger. It is a **logging infrastructure layer** embedded directly into your application. It automatically creates, manages, rotates, and retains logs. Best of all, it provides a built-in UI to view those logs directly from your application without needing external services like ELK, Datadog, or CloudWatch.

### 🚀 Features So Far
- **Zero-configuration setup:** Works out of the box.
- **Automatic `TraceNestLogs/` folder creation:** No need to setup directories manually.
- **Day-wise or single-file logging modes:** Flexible storage options.
- **Strict size and retention enforcement:** Automatically rotates and deletes old logs.
- **Built-In UI:** A beautiful, responsive, and dark-mode compatible UI served directly from your app.
- **Native FastAPI middleware:** Automatically captures HTTP requests and unhandled exceptions.
- **Built-in Secret Redaction:** Prevents credentials, API keys, and passwords from leaking.
- **High Performance:** Buffered I/O and background threads ensure your app never slows down.

---

## 🗂️ Types of Logs Managed

TraceNest handles several types of logs out of the box. We provide comprehensive application log levels for every scenario:

1. **Application Logs:** Custom log methods you can call directly from your code:
   - `logger.trace("Deep execution flow")` - For highly detailed, granular execution tracking.
   - `logger.debug("Variable state check")` - For diagnostic information useful during development.
   - `logger.info("User logged in")` - For general application events and standard milestones.
   - `logger.warning("Disk space low")` - For unexpected situations that aren't yet fatal errors.
   - `logger.error("Payment failed")` - For explicit failures that affect a specific operation.
   - `logger.critical("System crash")` - For catastrophic failures requiring immediate attention.
2. **HTTP Request Logs:** (When using FastAPI) Automatically logs all incoming requests, response HTTP status codes, request URLs, client IP addresses, and exact request durations.
3. **Exception Logs:** Automatically captures all unhandled exceptions, including full stack tracebacks, so you never lose debugging context when things break.
4. **Security Logs:** Silently handles sensitive data by recursively searching and masking secrets like `Authorization` headers, JWT tokens, user passwords, and database connection URIs before they are ever stored.

---

## ⚙️ Installation & Implementation

### 1. Installation

Install TraceNest via pip:
```bash
pip install tracenest
```

### 2. Basic Python Implementation

For a standard Python application or script, simply import the logger and use it.

```python
from tracenest import logger

# TraceNest automatically initializes and creates the TraceNestLogs/ folder
logger.info("Application started successfully")

try:
    1 / 0
except Exception as e:
    logger.error("A critical error occurred", error=str(e))
```

### 3. FastAPI Implementation (with UI and Middleware)

To fully leverage TraceNest in a FastAPI application, integrate the middleware and the UI router.

```python
from fastapi import FastAPI
from tracenest.fastapi import TraceNestMiddleware, setup_tracenest
from tracenest import logger

app = FastAPI()

# 1. Add Middleware to log all HTTP requests automatically
app.add_middleware(TraceNestMiddleware)

# 2. Setup the TraceNest UI (Access it at http://localhost:8000/tracenest)
setup_tracenest(app)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}
```

*After running your FastAPI app, visit `http://localhost:8000/tracenest` to see your logs in real-time!*

---

## 🛠️ How it Works (For Developers)

When you install and import TraceNest into your project, it seamlessly injects itself into your application lifecycle.

### Step-by-Step Developer Workflow
1. **Import:** The moment `from tracenest import logger` is executed, TraceNest's core initializes.
2. **Initialization:** It checks for the existence of `TraceNestLogs/` in your root directory. If missing, it creates it.
3. **Queue Creation:** It spawns a background thread and an in-memory queue to handle log writing without blocking your main application thread.
4. **Middleware Injection:** When `TraceNestMiddleware` is added, it wraps around the ASGI application to intercept all incoming requests.
5. **UI Mounting:** When `setup_tracenest(app)` is called, TraceNest mounts static files and API routes to serve the dashboard.

### Architecture Diagram

```text
[Your Application code] --(logger.info)--> [TraceNest In-Memory Queue]
[Incoming HTTP Request] --(Intercepted)--> [TraceNest Middleware] --> [TraceNest In-Memory Queue]

[TraceNest In-Memory Queue] --(Background Thread Flushes)--> [TraceNestLogs / YYYY-MM-DD.log]

[Developer Browser] --(http://localhost:8000/tracenest)--> [TraceNest UI Router] --(Reads)--> [TraceNestLogs]
```

---

## 🔄 The TraceNest Lifecycle

Understanding the lifecycle of a single log message helps illustrate why TraceNest is safe and performant.

### Step-by-Step Lifecycle
1. **Capture:** A log event is generated via `logger.info()` or the `TraceNestMiddleware`.
2. **Redaction:** The event is immediately scanned for sensitive keys (e.g., passwords, tokens) and redacted.
3. **Buffering:** The structured log is placed into a thread-safe in-memory queue (O(1) operation). Your application continues executing immediately.
4. **Flushing:** A background worker thread wakes up periodically (or when the queue reaches a threshold) and writes the buffered logs to the disk sequentially.
5. **Rotation & Retention:** During the flush, TraceNest checks the file size and date. If the file is too large or it's a new day, it rotates the file and deletes logs older than the retention period (default 60 days).
6. **Streaming:** If a developer has the UI open, the UI periodically polls the TraceNest backend, which reads the latest logs from disk and streams them to the browser.

### Lifecycle Diagram

```text
Application -> TraceNest Core: logger.error("DB Timeout", password="secret123")
TraceNest Core -> Redaction Engine: Scan and Mask
Redaction Engine -> TraceNest Core: {"msg": "DB Timeout", "password": "***"}
TraceNest Core -> Memory Queue: Push to Buffer (Non-blocking)
Application -> Application: Continues Execution...

(Background Thread)
Memory Queue -> File System: Flush Buffer to File
File System -> File System: Check File Size / Rotate if needed

(Developer UI)
Developer UI -> TraceNest Core: GET /tracenest/api/logs
TraceNest Core -> File System: Read latest entries
File System -> Developer UI: Return JSON payload
Developer UI -> Developer UI: Render in Dashboard
```

---

## 🎨 Built-In UI

TraceNest provides a robust web UI out of the box:
- **Live log streaming:** Auto-refreshing dashboard.
- **Deep-dive details:** Slide-out panel for traceback and structured data.
- **Search and filtering:** Filter by log level (INFO, ERROR, etc.) or text search.
- **Themes:** Dark, Light, Dark Blue, Emerald, Ruby, Amethyst, and Midnight.

---

## 🔒 Security and Redaction

TraceNest includes built-in secret redaction. It recursively searches through dictionaries, lists, request data, and log strings to mask:
- Passwords
- API Keys
- JWT Tokens
- Authorization Headers
- Database connection strings

Logs are redacted **before** they hit the in-memory queue, ensuring secrets never touch the disk.

---

## 📜 Versioning & Changelog

TraceNest follows semantic versioning. Below is the complete history of changes:

### v0.1.16 - 2026-08-16

#### Added
* Massive documentation overhaul: Completely rewrote the `README.md` to include detailed explanations of TraceNest's architecture, types of logs managed, and implementation guides for both standalone Python and FastAPI projects.
* Included detailed Mermaid diagrams illustrating the Developer Workflow and the TraceNest Event Lifecycle.
* Comprehensive feature summary highlighting security (redaction), UI themes, and performance guarantees.

#### Fixed
* TraceNest UI crashing backend issue: Fixed the import path for `setup_tracenest` to properly mount the TraceNest UI and API router.
* MongoDB connection failure: Commented out the `MONGODB_ATLAS_URI` in `.env` to fallback seamlessly to the local Docker MongoDB instance.
* Validated frontend health checks and TraceNest log generation in the `TraceNestLogs` directory.

### v0.1.15 - 2026-07-16

#### Added
* Injected **Under the Hood** sections into all 14 documentation chapters. This adds deep technical depth, explaining thread queues, AST logic, regex compilation, and FastAPI dependency injection mechanics to satisfy advanced developers while keeping the primary guide layman-friendly.

### v0.1.14 - 2026-07-16

#### Fixed
* Fixed a Mermaid syntax error in the documentation (`01_introduction.md`) that caused the high-level architecture diagram to fail to render on GitHub.

### v0.1.13 - 2026-07-16

#### Added
* Completely rebuilt the `docs/` folder with an exhaustive, beginner-friendly 14-chapter Master Guide! Everything from core concepts (Configuration, Formatter, Retention, Rotation) to Advanced Customizations and Troubleshooting is now thoroughly explained with examples and diagrams.

### v0.1.12 - 2026-07-15

#### Fixed
* Fixed z-index issue causing the dropdown menus (Levels and Themes) to incorrectly render underneath the sticky table headers. 

### v0.1.11 - 2026-07-15

#### Added
* 4 Beautiful New Themes: Emerald (Green), Ruby (Red), Amethyst (Purple), and Midnight (OLED High Contrast).
* Redesigned footer showcasing the current TraceNest version and developer credit.

#### Fixed
* Fixed search input box retaining a white background when using dark themes.

### v0.1.10 - 2026-07-15

#### Fixed
* Fixed white background issue on table rows and dropdown menus when using Dark or Dark Blue themes. All components now properly inherit theme colors.

### v0.1.9 - 2026-07-15

#### Fixed
* Fatal UI crash preventing logs from displaying on fresh installs due to a DOM mismatch.
* Replaced inline level badges with a clean dropdown menu for improved UX.
* Removed the "Versions" modal entirely for a simpler, decluttered interface.

### v0.1.8 - 2026-07-15

#### Added
* Auto-refresh functionality to stream logs live in the dashboard without manually reloading.
* Manual refresh button.
* Slide-out Details Panel providing deep-dive capabilities into structured logs and traceback without losing table context.
* PyPI version checking directly in the UI versions modal.

#### UI
* Completely redesigned UI dashboard inspired by modern observability platforms (e.g., Grafana/Vercel).
* High contrast, beautiful themes (Dark, Light, Dark Blue) relying on modern `CSS variables`.
* Refined typography utilizing Inter and JetBrains Mono fonts.
* Advanced layout featuring fixed-width columns and custom level badges.

#### Fixed
* Current log selection bug: Re-rendering the dashboard on polling no longer destroys user selection.
* DOM flickering issues eliminated.

#### Performance
* Achieved O(1) table updates per polling interval by intelligently caching parsed logs and dynamically computing diffs on the frontend.

#### Breaking Changes
* None

### v0.1.7 - 2026-07-03

#### Added
* Markdown-based changelog system directly integrated into the UI.
* Dynamic Versions modal featuring a beautiful two-pane layout, fetching and rendering markdown using `marked.js`.
* Synced main project `README.md` with the full project changelog to ensure release notes are visible directly on PyPI.

#### Changed
* Improved UI links, adding proper developer attribution linking back to GitHub in the UI footer.
* Removed the static `changelog.json` in favor of the dynamic API.

### v0.1.6 - 2026-07-03

#### Added
* Added built-in secret redaction to prevent credentials, tokens, API keys, cookies, and database passwords from leaking in logs.
* Added recursive masking for dictionaries, lists, nested metadata, request data, and response data.
* Added pattern-based masking for raw log strings, Authorization headers, JWTs, database URLs, Redis URLs, and key-value secrets.
* Added configuration options for custom sensitive keys and redaction mask.

#### Changed
* Logs are now redacted before storage and before UI/API display for defense-in-depth safety.
* Middleware logging now masks sensitive headers, cookies, request bodies, and response bodies.

#### Tests
* Added tests for key-based redaction, regex redaction, nested data structures, middleware safety, and custom redaction configuration.

---

## 🧑‍💻 Author & Maintainer

**VishwajitVM**

- 📍 New Delhi, India  
- 🐙 GitHub: https://github.com/vishwajitvm  
- ✉️ Email: vishwajitmall50@gmail.com  

TraceNest is actively maintained with a strong focus on real-world production use cases, developer experience, and long-term scalability.

---

## 📄 License

TraceNest SDK is free to use and distributed under the MIT license.
