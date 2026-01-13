import os
from pathlib import Path

from tracenest.core.rotation import rotate_if_needed
from tracenest.core.config import (
    ARCHIVE_DIR_NAME,
    LOG_FILE_EXTENSION,
    MAX_LOG_FILE_SIZE_BYTES,
)


def _write_bytes(p: Path, n: int) -> None:
    with open(p, "wb") as f:
        f.write(b"x" * n)


def test_no_rotation_below_threshold(tmp_path):
    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"
    _write_bytes(log_file, MAX_LOG_FILE_SIZE_BYTES - 1)

    rotate_if_needed(log_file)

    assert log_file.exists()
    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    assert not archive_dir.exists()


def test_rotation_triggers_and_moves_file(tmp_path):
    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"
    _write_bytes(log_file, MAX_LOG_FILE_SIZE_BYTES + 1)

    rotate_if_needed(log_file)

    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    assert archive_dir.exists()

    archived = list(archive_dir.iterdir())
    assert len(archived) == 1
    assert archived[0].name.startswith("2026-01-01_")
    assert archived[0].name.endswith(LOG_FILE_EXTENSION)
    assert not log_file.exists()


def test_rotation_is_idempotent(tmp_path):
    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"
    _write_bytes(log_file, MAX_LOG_FILE_SIZE_BYTES + 1)

    # Call multiple times
    rotate_if_needed(log_file)
    rotate_if_needed(log_file)
    rotate_if_needed(log_file)

    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    archived = list(archive_dir.iterdir())
    assert len(archived) == 1


def test_rotation_creates_next_index(tmp_path):
    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    archive_dir.mkdir(parents=True)

    # Pre-create an archived file to force index increment
    existing = archive_dir / f"2026-01-01_1{LOG_FILE_EXTENSION}"
    _write_bytes(existing, 10)

    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"
    _write_bytes(log_file, MAX_LOG_FILE_SIZE_BYTES + 5)

    rotate_if_needed(log_file)

    archived = sorted(p.name for p in archive_dir.iterdir())
    assert f"2026-01-01_2{LOG_FILE_EXTENSION}" in archived


def test_rotation_does_not_overwrite_existing_archive(tmp_path):
    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    archive_dir.mkdir(parents=True)

    # Occupy index 1
    occupied = archive_dir / f"2026-01-01_1{LOG_FILE_EXTENSION}"
    _write_bytes(occupied, 10)

    # Create oversized log
    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"
    _write_bytes(log_file, MAX_LOG_FILE_SIZE_BYTES + 10)

    rotate_if_needed(log_file)

    # Original archive must remain untouched
    assert occupied.exists()


def test_rotation_handles_missing_file_gracefully(tmp_path):
    log_file = tmp_path / f"2026-01-01{LOG_FILE_EXTENSION}"

    # Should not raise
    rotate_if_needed(log_file)

    archive_dir = tmp_path / ARCHIVE_DIR_NAME
    assert not archive_dir.exists()
