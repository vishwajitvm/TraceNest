import json
import threading
import time

from tracenest.logger import logger
from tracenest.core.formatter import format_log


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

class _CaptureWriter:
    """
    Test double to capture log lines without touching filesystem.
    """
    def __init__(self):
        self.lines = []

    def write(self, line: str) -> None:
        self.lines.append(line)


def _install_capture_writer(monkeypatch):
    """
    Monkeypatch the writer used by logger to capture output.
    """
    from tracenest import logger as logger_module

    cap = _CaptureWriter()

    def _fake_get_writer():
        return cap

    monkeypatch.setattr(logger_module, "_get_writer", _fake_get_writer)
    return cap


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_invalid_log_level_is_normalized(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    logger.log("whatever", "hello")

    assert len(cap.lines) == 1
    data = json.loads(cap.lines[0])
    assert data["level"] == "INFO"


def test_alias_log_levels(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    logger.log("warn", "a")
    logger.log("err", "b")
    logger.log("fatal", "c")

    levels = [json.loads(l)["level"] for l in cap.lines]
    assert levels == ["WARNING", "ERROR", "CRITICAL"]


def test_metadata_garbage_is_safe(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    logger.info("test", a=object(), b=set([1, 2]))

    data = json.loads(cap.lines[0])
    assert "meta" in data
    assert "a" in data["meta"]
    assert "b" in data["meta"]


def test_exception_argument_is_logged(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    try:
        1 / 0
    except Exception as e:
        logger.error("fail", exception=e)

    data = json.loads(cap.lines[0])
    assert "exc" in data
    assert "stack" in data["exc"]


def test_exc_info_true_is_logged(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    try:
        1 / 0
    except Exception:
        logger.error("fail", exc_info=True)

    data = json.loads(cap.lines[0])
    assert "exc" in data
    assert "stack" in data["exc"]


def test_recursive_logging_is_prevented(monkeypatch):
    """
    If writer.write triggers another log call, recursion must stop.
    """
    from tracenest import logger as logger_module

    calls = {"count": 0}

    class RecursiveWriter:
        def write(self, line: str) -> None:
            calls["count"] += 1
            # Attempt recursive logging
            logger.info("recursive")

    def _fake_get_writer():
        return RecursiveWriter()

    monkeypatch.setattr(logger_module, "_get_writer", _fake_get_writer)

    logger.info("start")

    # Only the first write should happen
    assert calls["count"] == 1


def test_thread_safety_under_concurrency(monkeypatch):
    cap = _install_capture_writer(monkeypatch)

    def worker():
        for _ in range(100):
            logger.info("x")

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(cap.lines) == 500
