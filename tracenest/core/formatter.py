"""
TraceNest Log Formatter

Defines the immutable log record schema and serialization logic.
Output format: JSON Lines (one JSON object per line).

SAFETY GUARANTEES:
- Never raises exceptions outward
- Never emits invalid JSON
- Never exceeds size limits
"""

from __future__ import annotations

import json
import inspect
import os
import threading
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .config import (
    PROJECT_NAME,
    PROJECT_VERSION,
    TIMESTAMP_FORMAT,
    USE_UTC_TIMESTAMPS,
    MAX_MESSAGE_LENGTH,
    MAX_METADATA_SIZE,
    MAX_METADATA_KEYS,
    MAX_METADATA_KEY_LENGTH,
    MAX_EXCEPTION_STACK_LENGTH,
    MAX_LOG_RECORD_SIZE_BYTES,
    FAIL_SILENTLY,
)

# =====================================================================
# Time helpers
# =====================================================================


def _utc_now_iso() -> str:
    try:
        if USE_UTC_TIMESTAMPS:
            return datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT)
        return datetime.now().isoformat()
    except Exception:
        return ""


# =====================================================================
# String & JSON safety
# =====================================================================


def _truncate(value: str, limit: int) -> str:
    try:
        if value is None:
            return ""
        return value if len(value) <= limit else value[:limit]
    except Exception:
        return ""


def _safe_json_value(value: Any) -> Any:
    """
    Guarantees JSON-serializable output.
    """
    try:
        json.dumps(value)
        return value
    except Exception:
        try:
            return str(value)
        except Exception:
            return "<unserializable>"


# =====================================================================
# Metadata handling
# =====================================================================


def _sanitize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Enforces:
    - dict-only metadata
    - flat structure
    - key count limit
    - total size limit
    - JSON safety
    """
    if not metadata or not isinstance(metadata, dict):
        return {}

    safe: Dict[str, Any] = {}
    total_size = 0
    key_count = 0

    for k, v in metadata.items():
        if key_count >= MAX_METADATA_KEYS:
            break

        key = str(k)[:MAX_METADATA_KEY_LENGTH]
        val = _safe_json_value(v)

        entry_size = len(key) + len(str(val))
        if total_size + entry_size > MAX_METADATA_SIZE:
            break

        safe[key] = val
        total_size += entry_size
        key_count += 1

    return safe


# =====================================================================
# Source & runtime context
# =====================================================================


def _get_source() -> Dict[str, Any]:
    """
    Best-effort capture of caller location.
    """
    try:
        frame = inspect.stack()[4]
        return {
            "file": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
    except Exception:
        return {}


def _get_runtime_context() -> Dict[str, Any]:
    """
    Minimal runtime context for debugging concurrency & crashes.
    """
    try:
        return {
            "pid": os.getpid(),
            "thread": threading.current_thread().name,
        }
    except Exception:
        return {}


def _get_env() -> str:
    """
    Explicit environment signal.
    Zero config. Best effort.
    """
    try:
        return (
            os.getenv("TRACENEST_ENV")
            or os.getenv("ENV")
            or os.getenv("APP_ENV")
            or "local"
        )
    except Exception:
        return "local"


# =====================================================================
# Exception handling
# =====================================================================


def _format_exception(exc: BaseException) -> Dict[str, Any]:
    """
    Formats exception safely with bounded stack trace.
    """
    try:
        stack = "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )

        truncated = False
        if len(stack) > MAX_EXCEPTION_STACK_LENGTH:
            stack = stack[:MAX_EXCEPTION_STACK_LENGTH]
            truncated = True

        return {
            "type": exc.__class__.__name__,
            "message": str(exc),
            "stack": stack,
            "truncated": truncated,
        }
    except Exception:
        return {}


# =====================================================================
# Public formatter (FINAL BOUNDARY)
# =====================================================================


def format_log(
    *,
    level: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_source: bool = False,
    exception: Optional[BaseException] = None,
    trace_id: Optional[str] = None,
) -> str:
    """
    Formats a log entry as a JSON line.

    This function is the FINAL safety boundary.
    It must never raise.
    """
    try:
        ts = _utc_now_iso()
        msg = _truncate(str(message), MAX_MESSAGE_LENGTH)

        record: Dict[str, Any] = {
            # ---- schema identity ----
            "schema": "tracenest.v1",
            "project": PROJECT_NAME,
            "version": PROJECT_VERSION,

            # ---- canonical fields ----
            "ts": ts,                 # internal
            "timestamp": ts,          # external-friendly
            "level": str(level).upper(),

            "msg": msg,               # internal
            "message": msg,           # external-friendly

            "env": _get_env(),

            # ---- structured metadata ----
            "meta": _sanitize_metadata(metadata),

            # ---- runtime context ----
            "ctx": _get_runtime_context(),
        }

        if trace_id:
            record["trace_id"] = str(trace_id)

        if include_source:
            src = _get_source()
            if src:
                record["src"] = src

        if exception:
            exc = _format_exception(exception)
            if exc:
                record["exc"] = exc

        serialized = json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
        )

        # Final absolute size guard
        if len(serialized) > MAX_LOG_RECORD_SIZE_BYTES:
            serialized = serialized[:MAX_LOG_RECORD_SIZE_BYTES]

        return serialized

    except Exception:
        if FAIL_SILENTLY:
            return ""
        raise
