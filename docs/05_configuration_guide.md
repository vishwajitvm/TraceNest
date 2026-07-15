# 05. Configuration Guide

TraceNest works great right out of the box, but you can customize almost everything about it using the `TraceNestConfig` class.

## The Default Settings
If you don't provide a configuration, TraceNest uses these defaults:

* **Log Folder:** A folder named `logs/` in your current directory.
* **Log File:** `app.log`.
* **Max File Size (Rotation):** 10 Megabytes (`10 * 1024 * 1024` bytes).
* **Retention Days:** 7 days.
* **Secret Redaction:** Enabled (hides passwords and API keys).

## How to Custom Configure TraceNest

To change the settings, you simply create a `TraceNestConfig` object and pass it to `get_logger()`.

```python
from tracenest.logger import get_logger
from tracenest.core.config import TraceNestConfig

# 1. Create your custom configuration
my_config = TraceNestConfig(
    log_dir="/var/log/my_company",   # Save logs to a specific system folder
    log_file_name="api_server.log",  # Name the file api_server.log
    max_bytes=50 * 1024 * 1024,      # Rotate the file when it hits 50 MB
    backup_count=30,                 # Keep up to 30 old log files (Retention)
    mask_secrets=True                # Make sure passwords are hidden
)

# 2. Pass the config to the logger
logger = get_logger("my_api", config=my_config)

logger.info("Custom logger initialized!")
```

## Configuration Cheat Sheet

Here is a quick reference of every setting you can change in `TraceNestConfig`:

| Setting | Type | Default | What it does |
| :--- | :--- | :--- | :--- |
| `log_dir` | `str` | `"logs"` | The folder where your log files will be saved. |
| `log_file_name` | `str` | `"app.log"` | The name of the main log file. |
| `max_bytes` | `int` | `10485760` (10MB) | How big the log file can get before it creates a new one (Rotation). |
| `backup_count` | `int` | `7` | How many old log files to keep before deleting them (Retention). |
| `mask_secrets` | `bool` | `True` | Whether to scan logs for things like "password=123" and turn it into "password=***" |

## Under the Hood (Technical Context)
When you pass the `TraceNestConfig` object to `get_logger()`, here is exactly what the initialization sequence does:
1. Validates the configuration using the `@dataclass` fields.
2. Resolves `log_dir` into a fully absolute `pathlib.Path` object.
3. Automatically executes `Path.mkdir(parents=True, exist_ok=True)` to guarantee the logging directory exists before any IO operations attempt to write to it.
4. If `mask_secrets` is `True`, it injects the `SecretRedactor` filter directly into the `TraceNestJsonFormatter`.

---
**Next Step:** Learn how to connect this to a web server in [06. FastAPI Integration](06_fastapi_integration.md).
