import os
from pathlib import Path

import pytest

from tracenest.core.writer import LogWriter
from tracenest.core.config import (
    LOG_FILE_EXTENSION,
    WRITE_BUFFER_SIZE,
    MAX_LOG_RECORD_SIZE_BYTES,
)
from tracenest.core.config import get_log_root_path


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _read_all_logs(log_root: Path) -> str:
    content = []
    for p in sorted(log_root.iterdir()):
        if p.is_file() and p.name.endswith(LOG_FILE_EXTENSION):
            content.append(p.read_text(encoding="utf-8", errors="replace"))
    return "".join(content)


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_writer_creates_log_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    assert log_root.exists()
    assert log_root.is_dir()


def test_writer_buffers_and_flushes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    for i in range(WRITE_BUFFER_SIZE):
        writer.write(f"line-{i}")

    # Buffer should flush automatically at threshold
    content = _read_all_logs(log_root)
    for i in range(WRITE_BUFFER_SIZE):
        assert f"line-{i}\n" in content


def test_writer_manual_flush(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    writer.write("hello")
    writer.flush()

    content = _read_all_logs(log_root)
    assert "hello\n" in content


def test_oversized_single_line_is_dropped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    big = "x" * (MAX_LOG_RECORD_SIZE_BYTES + 10)
    writer.write(big)
    writer.flush()

    content = _read_all_logs(log_root)
    assert content == ""


def test_writer_survives_file_deletion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    writer.write("before")
    writer.flush()

    # Delete log file manually
    for p in log_root.iterdir():
        if p.is_file():
            p.unlink()

    writer.write("after")
    writer.flush()

    content = _read_all_logs(log_root)
    assert "after\n" in content


def test_writer_fork_safety_reinitializes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    writer.write("parent")
    writer.flush()

    # Simulate fork by changing PID
    writer._pid = -1  # force mismatch
    writer.write("child")
    writer.flush()

    content = _read_all_logs(log_root)
    assert "child\n" in content


def test_writer_drops_buffer_on_write_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    writer = LogWriter()
    log_root = get_log_root_path()

    # Force open() to fail
    def _bad_open(*args, **kwargs):
        raise OSError("disk error")

    monkeypatch.setattr("builtins.open", _bad_open)

    writer.write("x")
    writer.flush()

    # Restore open and ensure no stale buffer retries
    monkeypatch.undo()

    writer.write("y")
    writer.flush()

    content = _read_all_logs(log_root)
    assert "y\n" in content
