# Secret Redaction / Credential Masking

TraceNest now includes a built-in secret redaction and credential masking engine to prevent sensitive data from leaking into logs or being exposed via the UI.

## Why this change was needed
Logs often inadvertently capture sensitive information like database passwords, API keys, JWT tokens, and user credentials. If these logs are stored or viewed, they become a security risk. By implementing an automated redaction system, TraceNest guarantees that sensitive information is securely masked before being logged or displayed, providing a "safe by default" experience.

## Dual-Layer Defense-in-Depth Architecture

TraceNest applies redaction at two distinct layers to ensure maximum safety:

```mermaid
graph TD
    A[Application Logs] -->|Metadata / Exception| B(Formatter)
    B -->|redact_any & redact_string| C(Write to Disk)
    C -->|Stored Log File| D
    D -->|Read Log| E(UI Router)
    E -->|redact_string| F[Frontend UI]
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
```

1. **Write Path (Formatter):** Before a log line is serialized to JSON and written to disk, all metadata dictionaries, exception contexts, and message strings are recursively scanned and redacted.
2. **Read Path (UI Router):** Before serving log files to the frontend UI via the `/api/logs` endpoint, each line is passed through the string redactor again. This ensures that even if a secret somehow slipped into the file (e.g., from an external process), it will not be displayed to the user.

## Files Changed

- `tracenest/core/config.py`: Added security configuration options like `MASK_SECRETS`, `REDACTION_MASK`, and `SENSITIVE_KEYS`.
- `tracenest/security/redaction.py` **[NEW]**: The core redaction engine containing functions to redact strings via regex, and recursively redact dictionaries and lists.
- `tracenest/core/formatter.py`: Integrated the redaction engine to sanitize metadata, exceptions, and the final JSON string before disk write.
- `tracenest/fastapi/middleware.py`: Updated request logging to capture and automatically redact request headers and cookies.
- `tracenest/ui/router.py`: Integrated the redaction engine to sanitize log files upon read.
- `tests/test_redaction.py` **[NEW]**: Unit tests for verifying correct masking of strings, URLs, dicts, and arrays.

## How Secret Masking Works

The engine uses two primary methods:
- **Key-based Matching**: Any dictionary key matching the `SENSITIVE_KEYS` set (case-insensitive) will have its value replaced with the `REDACTION_MASK` (default: `********`).
- **Pattern-based Matching**: Raw strings are scanned using Regex to identify and mask:
  - `Authorization: Bearer <token>`
  - Key-value assignments like `PASSWORD=abc123`
  - JSON-style assignments like `"api_key": "secret"`
  - Database connection URIs (e.g., `postgresql://user:password@host/db`)

## How to Configure

Secret redaction is **enabled by default** (`MASK_SECRETS = True`).

To customize the sensitive keys, you can modify `SENSITIVE_KEYS` in your TraceNest configuration:

```python
from tracenest.core.config import SENSITIVE_KEYS

SENSITIVE_KEYS.add("my_custom_secret_key")
```

To disable it (Not recommended in production):
```python
from tracenest.core.config import MASK_SECRETS
MASK_SECRETS = False
```

## How to Test

Run the test suite using pytest:
```bash
python -m pytest tests/
```

## Release Commands Used

```bash
git add .
git commit -m "feat: add secret redaction for safe logging"
git tag v0.1.6
git push origin main
git push origin v0.1.6
python -m build
twine check dist/*
twine upload dist/*
```
