"""
TraceNest Log Rotation

Handles size-based rotation of log files.

SAFETY GUARANTEES:
- Never raises exceptions outward
- Idempotent (safe to call repeatedly)
- Collision-safe
- Best-effort only
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from .config import (
    ARCHIVE_DIR_NAME,
    LOG_FILE_EXTENSION,
    MAX_LOG_FILE_SIZE_BYTES,
    MAX_ROTATED_FILES_PER_DAY,
    FAIL_SILENTLY,
)

# =====================================================================
# Internal state (minimal & bounded)
# =====================================================================

# Prevent rotation storms (best-effort, per-process)
_LAST_ROTATION_ATTEMPT: dict[Path, float] = {}
_ROTATION_COOLDOWN_SECONDS = 1.0  # small, safe cooldown


# =====================================================================
# Public API
# =====================================================================


def rotate_if_needed(log_file: Path) -> None:
    """
    Rotates the given log file if it exceeds size limits.

    Safe to call multiple times.
    """
    try:
        # Fast exit if file missing
        if not log_file.exists():
            return

        # Ignore empty or tiny files
        try:
            size = log_file.stat().st_size
        except Exception:
            return

        if size <= 0 or size < MAX_LOG_FILE_SIZE_BYTES:
            return

        # Rotation cooldown guard
        now = time.time()
        last = _LAST_ROTATION_ATTEMPT.get(log_file)
        if last and (now - last) < _ROTATION_COOLDOWN_SECONDS:
            return

        _LAST_ROTATION_ATTEMPT[log_file] = now

        _rotate(log_file)

    except Exception:
        if not FAIL_SILENTLY:
            raise


# =====================================================================
# Internal helpers
# =====================================================================


def _rotate(log_file: Path) -> None:
    """
    Performs the rotation operation (best-effort).
    """
    try:
        # File may disappear between checks
        if not log_file.exists():
            return

        # Size may have changed
        try:
            if log_file.stat().st_size < MAX_LOG_FILE_SIZE_BYTES:
                return
        except Exception:
            return

        archive_dir = log_file.parent / ARCHIVE_DIR_NAME
        archive_dir.mkdir(parents=True, exist_ok=True)

        base_name = log_file.stem  # YYYY-MM-DD
        index = _next_rotation_index(archive_dir, base_name)

        if index is None:
            # Rotation limit reached; do nothing
            return

        rotated_name = f"{base_name}_{index}{LOG_FILE_EXTENSION}"
        rotated_path = archive_dir / rotated_name

        # Never overwrite an existing archive
        if rotated_path.exists():
            return

        # Final existence check before replace
        if not log_file.exists():
            return

        # Atomic rename (best-effort)
        os.replace(log_file, rotated_path)

    except Exception:
        if not FAIL_SILENTLY:
            raise


def _next_rotation_index(archive_dir: Path, base_name: str) -> int | None:
    """
    Finds the next available rotation index for a given day.

    Returns None if rotation limit is reached.
    """
    try:
        used = set()

        for file in archive_dir.iterdir():
            if not file.is_file():
                continue

            name = file.name
            if not name.startswith(f"{base_name}_"):
                continue

            try:
                suffix = (
                    name.replace(base_name + "_", "")
                        .replace(LOG_FILE_EXTENSION, "")
                )
                used.add(int(suffix))
            except Exception:
                continue

        for i in range(1, MAX_ROTATED_FILES_PER_DAY + 1):
            if i not in used:
                return i

        return None

    except Exception:
        return None
