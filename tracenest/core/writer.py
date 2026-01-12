"""
TraceNest Log Writer

Responsible for safely writing formatted log lines to disk.

SAFETY GUARANTEES:
- Never raises exceptions outward
- Never blocks application execution
- Never retries failed writes
- Fork-safe (best effort)
- Shutdown-safe
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Optional

from .config import (
    LOG_FILE_DATE_FORMAT,
    LOG_FILE_EXTENSION,
    MAX_LOG_FILE_SIZE_BYTES,
    MAX_LOG_RECORD_SIZE_BYTES,
    WRITE_BUFFER_SIZE,
    FLUSH_ON_EXIT,
    FAIL_SILENTLY,
    ENABLE_ROTATION,
)
from .config import get_log_root_path
from .rotation import rotate_if_needed
from .retention import enforce_retention

# =====================================================================
# Writer
# =====================================================================


class LogWriter:
    """
    Buffered, thread-safe, best-effort log writer.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._buffer: list[str] = []
        self._current_file: Optional[Path] = None
        self._pid = os.getpid()
        self._shutting_down = False

        self._initialize()

        if FLUSH_ON_EXIT:
            try:
                import atexit
                atexit.register(self._shutdown_flush)
            except Exception:
                pass

    # -----------------------------------------------------------------
    # Initialization & lifecycle
    # -----------------------------------------------------------------

    def _initialize(self) -> None:
        try:
            log_root = get_log_root_path()
            log_root.mkdir(parents=True, exist_ok=True)

            self._current_file = self._resolve_log_file()

            # Run retention once per process start
            enforce_retention(log_root)

        except Exception:
            if not FAIL_SILENTLY:
                raise

    def _shutdown_flush(self) -> None:
        self._shutting_down = True
        try:
            self.flush()
        except Exception:
            pass

    # -----------------------------------------------------------------
    # File resolution
    # -----------------------------------------------------------------

    def _resolve_log_file(self) -> Path:
        from datetime import datetime

        date_str = datetime.utcnow().strftime(LOG_FILE_DATE_FORMAT)
        filename = f"{date_str}{LOG_FILE_EXTENSION}"

        return get_log_root_path() / filename

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def write(self, log_line: str) -> None:
        """
        Accepts a single formatted log line.
        """
        if not log_line or self._shutting_down:
            return

        # Drop oversized individual log lines
        if len(log_line) > MAX_LOG_RECORD_SIZE_BYTES:
            return

        try:
            # Fork detection (best effort)
            if os.getpid() != self._pid:
                with self._lock:
                    self._pid = os.getpid()
                    self._buffer.clear()
                    self._initialize()

            with self._lock:
                self._buffer.append(log_line)

                if len(self._buffer) >= WRITE_BUFFER_SIZE:
                    self._flush_locked()

        except Exception:
            if not FAIL_SILENTLY:
                raise

    # -----------------------------------------------------------------
    # Flush logic
    # -----------------------------------------------------------------

    def flush(self) -> None:
        if self._shutting_down:
            return

        try:
            with self._lock:
                self._flush_locked()
        except Exception:
            if not FAIL_SILENTLY:
                raise

    def _flush_locked(self) -> None:
        if not self._buffer:
            return

        try:
            # Re-resolve file daily
            new_file = self._resolve_log_file()
            if self._current_file != new_file:
                self._current_file = new_file

            # Ensure directory exists (file may have been deleted)
            self._current_file.parent.mkdir(parents=True, exist_ok=True)

            # Pre-write rotation check
            if ENABLE_ROTATION:
                rotate_if_needed(self._current_file)

            # Write buffer
            with open(self._current_file, "a", encoding="utf-8") as f:
                for line in self._buffer:
                    f.write(line)
                    f.write("\n")

            # Post-write safety check
            if ENABLE_ROTATION:
                rotate_if_needed(self._current_file)

            self._buffer.clear()

        except Exception:
            # Drop buffer permanently to avoid infinite retry loops
            self._buffer.clear()

            if not FAIL_SILENTLY:
                raise
