"""
TraceNest Core Configuration

This module defines all internal, immutable defaults used by TraceNest.
There is NO user-facing configuration in v0.x.

All values here are intentionally conservative, deterministic,
and production-safe.

This file is a CONTRACT.
"""

from pathlib import Path
from typing import Final

# =====================================================================
# Project Identity
# =====================================================================

PROJECT_NAME: Final[str] = "TraceNest"
PROJECT_VERSION: Final[str] = "0.1.x"

# =====================================================================
# Logging Directory & Paths
# =====================================================================

# Root directory where all logs are stored (relative to CWD)
LOG_ROOT_DIR_NAME: Final[str] = "TraceNestLogs"

# Directory for rotated / archived logs
ARCHIVE_DIR_NAME: Final[str] = "archive"

# Temporary directory name (future-safe, not mandatory in v0.x)
TEMP_DIR_NAME: Final[str] = ".tmp"


def get_log_root_path() -> Path:
    """
    Returns the absolute path to the TraceNest log root directory.

    Resolution strategy:
    - Relative to current working directory
    - Never environment-dependent
    """
    return Path.cwd() / LOG_ROOT_DIR_NAME


# =====================================================================
# Log File Naming & Format
# =====================================================================

# Day-wise log file naming format
LOG_FILE_DATE_FORMAT: Final[str] = "%Y-%m-%d"

# File extension for log files
LOG_FILE_EXTENSION: Final[str] = ".log"

# Separator used in rotated file names
ROTATED_FILE_SEPARATOR: Final[str] = "_"

# =====================================================================
# File Size & Rotation Policy
# =====================================================================

# Maximum size of a single log file (bytes)
# Default: 25 MB
MAX_LOG_FILE_SIZE_BYTES: Final[int] = 25 * 1024 * 1024

# Maximum number of rotated files per day
MAX_ROTATED_FILES_PER_DAY: Final[int] = 5

# Whether rotation is enabled
ENABLE_ROTATION: Final[bool] = True

# =====================================================================
# Retention Policy
# =====================================================================

# Number of days logs are retained
RETENTION_DAYS: Final[int] = 60

# Whether retention cleanup runs on startup
RETENTION_RUN_ON_STARTUP: Final[bool] = True

# Whether retention cleanup runs during runtime
RETENTION_RUN_ON_WRITE: Final[bool] = False

# =====================================================================
# Write & Buffering Behavior
# =====================================================================

# Number of log entries buffered before flushing to disk
WRITE_BUFFER_SIZE: Final[int] = 50

# Flush logs automatically on interpreter exit
FLUSH_ON_EXIT: Final[bool] = True

# Flush buffer immediately for ERROR and CRITICAL logs
FLUSH_ON_HIGH_SEVERITY: Final[bool] = True

# =====================================================================
# Threading & Concurrency
# =====================================================================

# Enable thread-safe writes
THREAD_SAFE_WRITES: Final[bool] = True

# Lock acquisition timeout (seconds)
WRITE_LOCK_TIMEOUT_SECONDS: Final[float] = 2.0

# =====================================================================
# Log Levels
# =====================================================================

LOG_LEVELS: Final[dict[str, int]] = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

DEFAULT_LOG_LEVEL: Final[str] = "INFO"

# Minimum log level allowed internally
MIN_LOG_LEVEL: Final[str] = "DEBUG"

# =====================================================================
# Log Record Schema Constraints
# =====================================================================

# Maximum allowed message length
MAX_MESSAGE_LENGTH: Final[int] = 10_000

# Maximum metadata size (characters)
MAX_METADATA_SIZE: Final[int] = 5_000

# Maximum number of metadata keys
MAX_METADATA_KEYS: Final[int] = 50

# Maximum length of a single metadata key
MAX_METADATA_KEY_LENGTH: Final[int] = 100

# =====================================================================
# Timestamp & Time Handling
# =====================================================================

# Use UTC timestamps internally
USE_UTC_TIMESTAMPS: Final[bool] = True

# ISO 8601 timestamp format
TIMESTAMP_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%S.%fZ"

# =====================================================================
# Safety & Failure Handling
# =====================================================================

# Never raise internal exceptions to user code
FAIL_SILENTLY: Final[bool] = True

# Fallback to stdout if file logging fails
FALLBACK_TO_STDOUT: Final[bool] = False

# Drop log entries if internal failure occurs
DROP_LOGS_ON_FAILURE: Final[bool] = True

# =====================================================================
# FastAPI Integration Defaults
# =====================================================================

# Enable FastAPI middleware logging by default
FASTAPI_MIDDLEWARE_ENABLED: Final[bool] = True

# Log request body size limit (bytes)
FASTAPI_MAX_BODY_LOG_SIZE: Final[int] = 4 * 1024  # 4 KB

# Paths excluded from FastAPI logging
FASTAPI_EXCLUDED_PATHS: Final[set[str]] = {
    "/tracenest",
    "/health",
}

# =====================================================================
# UI Defaults
# =====================================================================

# Enable built-in UI
UI_ENABLED: Final[bool] = True

# Default UI route
UI_ROUTE_PATH: Final[str] = "/tracenest"

# Maximum lines returned per UI request
UI_MAX_LINES_PER_REQUEST: Final[int] = 1_000

# =====================================================================
# Internal Diagnostics
# =====================================================================

# Enable internal health checks (not exposed to users)
ENABLE_INTERNAL_HEALTH_CHECKS: Final[bool] = True

# Log internal TraceNest errors
LOG_INTERNAL_ERRORS: Final[bool] = False
