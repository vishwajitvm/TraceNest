import os
import time
from pathlib import Path

from tracenest.core.retention import enforce_retention
from tracenest.core.config import (
    ARCHIVE_DIR_NAME,
    LOG_FILE_EXTENSION,
    LOG_FILE_DATE_FORMAT,
    RETENTION_DAYS,
)


def _touch_with_mtime(path: Path, mtime: float) -> None:
    path.write_text("x", encoding="utf-8")
    os.utime(path, (mtime, mtime))


def _today_name() -> str:
    from datetime import datetime
    today = datetime.utcnow().strftime(LOG_FILE_DATE_FORMAT)
    return f"{today}{LOG_FILE_EXTENSION}"


def test_retention_keeps_todays_log(tmp_path):
    log_root = tmp_path
    today = log_root / _today_name()
    _touch_with_mtime(today, time.time() - (RETENTION_DAYS + 10) * 86400)

    enforce_retention(log_root)

    assert today.exists()


def test_retention_deletes_old_root_logs(tmp_path):
    log_root = tmp_path
    old_ts = time.time() - (RETENTION_DAYS + 1) * 86400

    old_log = log_root / "2000-01-01.log"
    _touch_with_mtime(old_log, old_ts)

    enforce_retention(log_root)

    assert not old_log.exists()


def test_retention_ignores_non_log_files(tmp_path):
    log_root = tmp_path
    junk = log_root / "notes.txt"
    _touch_with_mtime(junk, time.time() - (RETENTION_DAYS + 10) * 86400)

    enforce_retention(log_root)

    assert junk.exists()


def test_retention_cleans_archive_directory(tmp_path):
    log_root = tmp_path
    archive = log_root / ARCHIVE_DIR_NAME
    archive.mkdir(parents=True)

    old_ts = time.time() - (RETENTION_DAYS + 5) * 86400
    archived_log = archive / "1999-12-31_1.log"
    _touch_with_mtime(archived_log, old_ts)

    enforce_retention(log_root)

    assert not archived_log.exists()


def test_retention_does_not_follow_symlinks(tmp_path):
    log_root = tmp_path
    target = tmp_path / "external.log"
    _touch_with_mtime(target, time.time() - (RETENTION_DAYS + 5) * 86400)

    symlink = log_root / "2001-01-01.log"
    symlink.symlink_to(target)

    enforce_retention(log_root)

    assert symlink.exists()
    assert target.exists()


def test_retention_is_idempotent(tmp_path):
    log_root = tmp_path
    old_ts = time.time() - (RETENTION_DAYS + 5) * 86400

    old_log = log_root / "2002-02-02.log"
    _touch_with_mtime(old_log, old_ts)

    enforce_retention(log_root)
    enforce_retention(log_root)
    enforce_retention(log_root)

    assert not old_log.exists()


def test_retention_cooldown_prevents_repeated_scans(tmp_path, monkeypatch):
    log_root = tmp_path
    old_ts = time.time() - (RETENTION_DAYS + 5) * 86400

    old_log = log_root / "2003-03-03.log"
    _touch_with_mtime(old_log, old_ts)

    # First run deletes the file
    enforce_retention(log_root)
    assert not old_log.exists()

    # Recreate file immediately
    _touch_with_mtime(old_log, old_ts)

    # Second run within cooldown should skip
    enforce_retention(log_root)
    assert old_log.exists()
