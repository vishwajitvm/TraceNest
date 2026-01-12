# TraceNest Directory Structure

## Complete Project Skeleton (Authoritative)

```text
tracenest/
├── tracenest/
│   ├── __init__.py
│   ├── logger.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── writer.py
│   │   ├── rotation.py
│   │   ├── retention.py
│   │   ├── formatter.py
│   │   └── config.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── templates/
│   │   └── static/
│   │       ├── css/
│   │       ├── js/
│   │       └── themes/
│   ├── fastapi/
│   │   ├── __init__.py
│   │   └── middleware.py
│   └── utils/
│       ├── __init__.py
│       ├── time.py
│       └── filesystem.py
│
├── docs/
│   ├── introduction.md
│   ├── quickstart.md
│   ├── configuration.md
│   ├── fastapi.md
│   ├── ui.md
│   ├── performance.md
│   ├── changelog.md
│   └── directory-structure.md
│
├── examples/
│   ├── basic.py
│   └── fastapi_app.py
│
├── tests/
│   ├── test_logger.py
│   ├── test_rotation.py
│   └── test_retention.py
│
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
└── Dockerfile
```

---

# TraceNest Directory Structure

This document defines the **official, fixed, and authoritative directory structure** for the TraceNest project.

This structure is a **long-term architectural contract**. Once adopted, it should not be changed casually. Any modification must be justified by a major version change.

---

## Project Root Layout

```text
tracenest/
├── tracenest/                    # Core SDK package (published to PyPI)
├── docs/                         # Project documentation
├── examples/                     # Usage examples
├── tests/                        # Automated tests
├── pyproject.toml                # Build & dependency configuration
├── README.md                     # Public project overview
├── LICENSE                       # Open-source license
├── .gitignore                    # Git exclusions
└── Dockerfile                    # Container support
```

---

## tracenest/ — Core SDK Package

This directory contains the **entire TraceNest runtime**. Only code inside this folder is shipped to users via PyPI.

```text
tracenest/
├── __init__.py
├── logger.py
├── core/
├── ui/
├── fastapi/
└── utils/
```

### Design Rules
- No application-specific code
- No environment-specific assumptions
- Safe to import in any Python runtime
- Must never crash the host application

---

## tracenest/__init__.py

Purpose:
- Exposes the **public SDK surface**
- Re-exports the logger instance

Rules:
- No logic
- No UI or FastAPI imports
- Must remain stable across versions

---

## tracenest/logger.py — Public Logger API

This file defines the **only supported logging interface** for users.

Responsibilities:
- Accept log messages
- Attach structured metadata
- Delegate work to the core engine

Constraints:
- No file I/O
- No framework imports
- No configuration parsing

Example:
```python
from tracenest import logger

logger.info("Application started")
logger.error("Payment failed", order_id=123)
```

---

## tracenest/core/ — Logging Engine

Contains the internal engine responsible for the **entire log lifecycle**.

```text
core/
├── __init__.py
├── writer.py
├── rotation.py
├── retention.py
├── formatter.py
└── config.py
```

### writer.py
- Buffered file writes
- Thread-safe
- Non-blocking behavior
- Never raises exceptions outward

### rotation.py
- Day-wise log rotation
- Size-based rotation
- Archive handling

### retention.py
- Retention enforcement
- Automatic cleanup
- Safe execution during runtime

### formatter.py
- Structured log schema
- Timestamp and metadata enrichment
- Consistent output format

### config.py
- Internal defaults only
- No user-facing configuration
- Centralized limits and constants

---

## tracenest/ui/ — Built-in Log Viewer

Provides a **read-only local UI** for inspecting logs.

```text
ui/
├── __init__.py
├── router.py
├── templates/
└── static/
```

### router.py
- FastAPI router
- Exposes `/tracenest` endpoint
- Read-only access

### templates/
- HTML templates
- Minimal rendering logic

### static/
- JavaScript
- CSS
- Themes (light, dark, blue-dark)

Rules:
- UI never writes logs
- UI must not block the application
- FastAPI dependency allowed here only

---

## tracenest/fastapi/ — FastAPI Integration

Framework-specific integration layer.

```text
fastapi/
├── __init__.py
└── middleware.py
```

### middleware.py
- Automatic request logging
- Response status tracking
- Request duration measurement
- Unhandled exception capture

Rules:
- FastAPI imports allowed only here
- Must not leak into core engine
- Optional dependency

---

## tracenest/utils/ — Shared Utilities

Pure helper utilities used internally.

```text
utils/
├── __init__.py
├── time.py
└── filesystem.py
```

### time.py
- Timestamp helpers
- Date formatting utilities

### filesystem.py
- Safe directory creation
- Cross-platform file handling

Rules:
- No business logic
- No framework dependencies

---

## docs/ — Documentation

```text
docs/
├── introduction.md
├── quickstart.md
├── configuration.md
├── fastapi.md
├── ui.md
├── performance.md
├── changelog.md
└── directory-structure.md
```

Purpose:
- Explain architecture and philosophy
- Define contracts
- Track changes and decisions

---

## examples/ — Usage Examples

```text
examples/
├── basic.py
└── fastapi_app.py
```

Rules:
- Only public API usage
- No internal imports
- Acts as living documentation

---

## tests/ — Automated Tests

```text
tests/
├── test_logger.py
├── test_rotation.py
└── test_retention.py
```

Purpose:
- Validate correctness
- Prevent regressions
- Guarantee stability

---

## Structural Guarantee

This directory structure guarantees:
- Clear separation of concerns
- Safe extensibility
- Minimal breaking changes
- Enterprise-grade maintainability

This structure should be treated as a **contract**, not a suggestion.

