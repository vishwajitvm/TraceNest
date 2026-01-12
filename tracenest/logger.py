"""
TraceNest Public Logger API

This module exposes the stable, user-facing logging interface.

CRITICAL GUARANTEES:
- Never raises exceptions outward
- Never blocks application execution
- Safe under extreme misuse
- Safe during interpreter shutdown
- No recursive or re-entrant logging
"""

from __future__ import annotations

import sys
import threading
from typing import Any, Dict, Optional

from .core.config import (
    LOG_LEVELS,
    DEFAULT_LOG_LEVEL,
    FAIL_SILENTLY,
)
from .core.formatter import format_log

# =====================================================================
# Internal safety guards
# =====================================================================

# Thread-local guard to prevent recursive logging
_thread_state = threading.local()

# Global shutdown flag
_IS_SHUTTING_DOWN = False


def _mark_shutting_down() -> None:
    global _IS_SHUTTING_DOWN
    _IS_SHUTTING_DOWN = True


# Register shutdown hook
try:
    import atexit
    atexit.register(_mark_shutting_down)
except Exception:
    pass


# =====================================================================
# Log level normalization
# =====================================================================

_LEVEL_ALIASES = {
    "WARN": "WARNING",
    "ERR": "ERROR",
    "FATAL": "CRITICAL",
}


def _normalize_level(level: Any) -> str:
    """
    Converts arbitrary developer input into a valid log level.
    """
    try:
        lvl = str(level).upper()
        lvl = _LEVEL_ALIASES.get(lvl, lvl)
        return lvl if lvl in LOG_LEVELS else DEFAULT_LOG_LEVEL
    except Exception:
        return DEFAULT_LOG_LEVEL


# =====================================================================
# Metadata normalization
# =====================================================================


def _normalize_metadata(metadata: Any) -> Optional[Dict[str, Any]]:
    """
    Ensures metadata is dict-like or None.
    """
    if metadata is None:
        return None
    if isinstance(metadata, dict):
        return metadata
    return {"value": metadata}


# =====================================================================
# Writer access (lazy, thread-safe)
# =====================================================================

_writer_lock = threading.Lock()
_writer_instance = None


def _get_writer():
    """
    Lazy-load writer to avoid import cycles and startup cost.
    """
    global _writer_instance

    if _writer_instance is None:
        with _writer_lock:
            if _writer_instance is None:
                try:
                    from .core.writer import LogWriter
                    _writer_instance = LogWriter()
                except Exception:
                    _writer_instance = None

    return _writer_instance


# =====================================================================
# Core logging function (single entry point)
# =====================================================================


def _log(
    *,
    level: Any,
    message: Any,
    metadata: Any = None,
    exception: Optional[BaseException] = None,
    exc_info: bool = False,
    include_source: bool = False,
    trace_id: Optional[str] = None,
) -> None:
    """
    Internal logging entry point.

    This function is the FINAL safety boundary.
    It must NEVER raise.
    """
    # Fast exit if shutting down
    if _IS_SHUTTING_DOWN:
        return

    # Prevent recursive logging
    if getattr(_thread_state, "in_log", False):
        return

    try:
        _thread_state.in_log = True

        normalized_level = _normalize_level(level)
        normalized_metadata = _normalize_metadata(metadata)

        # exc_info=True support
        if exc_info and exception is None:
            exception = sys.exc_info()[1]

        log_line = format_log(
            level=normalized_level,
            message=str(message),
            metadata=normalized_metadata,
            include_source=include_source,
            exception=exception,
            trace_id=trace_id,
        )

        if not log_line:
            return

        writer = _get_writer()
        if writer:
            writer.write(log_line)
        # else: intentionally drop

    except Exception:
        if not FAIL_SILENTLY:
            raise
    finally:
        _thread_state.in_log = False


# =====================================================================
# Public Logger API
# =====================================================================


class Logger:
    """
    Public Logger Interface.

    This class is intentionally minimal and stable.
    """

    def debug(self, message: Any, **metadata: Any) -> None:
        _log(level="DEBUG", message=message, metadata=metadata)

    def info(self, message: Any, **metadata: Any) -> None:
        _log(level="INFO", message=message, metadata=metadata)

    def warning(self, message: Any, **metadata: Any) -> None:
        _log(level="WARNING", message=message, metadata=metadata)

    def error(
        self,
        message: Any,
        *,
        exception: Optional[BaseException] = None,
        exc_info: bool = False,
        **metadata: Any,
    ) -> None:
        _log(
            level="ERROR",
            message=message,
            metadata=metadata,
            exception=exception,
            exc_info=exc_info,
        )

    def critical(
        self,
        message: Any,
        *,
        exception: Optional[BaseException] = None,
        exc_info: bool = False,
        **metadata: Any,
    ) -> None:
        _log(
            level="CRITICAL",
            message=message,
            metadata=metadata,
            exception=exception,
            exc_info=exc_info,
        )

    def log(
        self,
        level: Any,
        message: Any,
        *,
        exception: Optional[BaseException] = None,
        exc_info: bool = False,
        include_source: bool = False,
        trace_id: Optional[str] = None,
        **metadata: Any,
    ) -> None:
        """
        Generic logging method.
        Accepts ANY level and ANY message safely.
        """
        _log(
            level=level,
            message=message,
            metadata=metadata,
            exception=exception,
            exc_info=exc_info,
            include_source=include_source,
            trace_id=trace_id,
        )


# =====================================================================
# Public singleton
# =====================================================================

logger = Logger()
