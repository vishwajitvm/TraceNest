"""
TraceNest Log Retention

Responsible for enforcing log retention policies.

SAFETY GUARANTEES:
- Never deletes active log files
- Never deletes directories
- Never follows symlinks
- Never raises exceptions outward
- Best-effort cleanup only
- Idempotent and safe to call repeatedly
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from .config import (
    RETENTION_DAYS,
    ARCHIVE_DIR_NAME,
    LOG_FILE_EXTENSION,
    FAIL_SILENTLY,
    LOG_FILE_DATE_FORMAT,
)

# =====================================================================
# Internal state (minimal & bounded)
# =====================================================================

_LAST_RETENTION_RUN: Optional[float] = None
_RETENTION_COOLDOWN_SECONDS = 60.0  # run at most once per minute


# =====================================================================
# Public API
# =====================================================================


def enforce_retention(log_root: Path) -> None:
    """
    Enforces retention policy on the given log root directory.

    Safe to call:
    - at startup
    - periodically
    - multiple times
    """
    global _LAST_RETENTION_RUN

    try:
        now = time.time()

        # Cooldown guard to prevent retention storms
        if _LAST_RETENTION_RUN and (now - _LAST_RETENTION_RUN) < _RETENTION_COOLDOWN_SECONDS:
            return
        _LAST_RETENTION_RUN = now

        if not log_root.exists() or not log_root.is_dir():
            return

        cutoff_ts = _retention_cutoff_timestamp(now)
        if cutoff_ts is None:
            return

        # 1. Clean archive directory first
        archive_dir = log_root / ARCHIVE_DIR_NAME
        if archive_dir.exists() and archive_dir.is_dir():
            _clean_directory(archive_dir, cutoff_ts, allow_all_logs=True)

        # 2. Clean old daily log files in root (excluding today)
        _clean_root_logs(log_root, cutoff_ts)

    except Exception:
        if not FAIL_SILENTLY:
            raise


# =====================================================================
# Internal helpers
# =====================================================================


def _retention_cutoff_timestamp(now: float) -> Optional[float]:
    """
    Returns the UNIX timestamp before which files should be deleted.

    Returns None if retention is disabled or invalid.
    """
    try:
        if RETENTION_DAYS <= 0:
            return None

        seconds = RETENTION_DAYS * 24 * 60 * 60
        cutoff = now - seconds

        # Guard against clock skew or absurd values
        if cutoff <= 0:
            return None

        return cutoff

    except Exception:
        return None


def _clean_directory(
    directory: Path,
    cutoff_ts: float,
    *,
    allow_all_logs: bool,
) -> None:
    """
    Deletes files older than cutoff_ts in the given directory.

    Directories are never deleted.
    Symlinks are never followed.
    """
    try:
        for item in directory.iterdir():
            try:
                if not item.is_file():
                    continue

                if item.is_symlink():
                    continue

                # Only delete TraceNest log files
                if not allow_all_logs and not _looks_like_tracenest_log(item.name):
                    continue

                stat = item.stat()
                if stat.st_mtime < cutoff_ts:
                    item.unlink(missing_ok=True)

            except Exception:
                continue

    except Exception:
        if not FAIL_SILENTLY:
            raise


def _clean_root_logs(log_root: Path, cutoff_ts: float) -> None:
    """
    Cleans old daily log files from the log root directory.

    IMPORTANT:
    - Never deletes today's active log file
    """
    try:
        today_name = _today_log_name()

        for item in log_root.iterdir():
            try:
                if not item.is_file():
                    continue

                if item.is_symlink():
                    continue

                if item.name == today_name:
                    continue

                if not _looks_like_tracenest_log(item.name):
                    continue

                stat = item.stat()
                if stat.st_mtime < cutoff_ts:
                    item.unlink(missing_ok=True)

            except Exception:
                continue

    except Exception:
        if not FAIL_SILENTLY:
            raise


def _looks_like_tracenest_log(filename: str) -> bool:
    """
    Returns True if the filename matches TraceNest log naming.
    """
    if not filename.endswith(LOG_FILE_EXTENSION):
        return False

    # Expected format: YYYY-MM-DD.log
    try:
        date_part = filename.replace(LOG_FILE_EXTENSION, "")
        time.strptime(date_part, LOG_FILE_DATE_FORMAT)
        return True
    except Exception:
        return False


def _today_log_name() -> str:
    """
    Returns today's active log file name.
    """
    from datetime import datetime

    today = datetime.utcnow().strftime(LOG_FILE_DATE_FORMAT)
    return f"{today}{LOG_FILE_EXTENSION}"
