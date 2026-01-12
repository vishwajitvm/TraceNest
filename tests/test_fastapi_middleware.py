import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tracenest.fastapi.middleware import TraceNestMiddleware
from tracenest.core.config import FASTAPI_EXCLUDED_PATHS
from tracenest.logger import logger


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

class _CaptureWriter:
    def __init__(self):
        self.lines = []

    def write(self, line: str) -> None:
        self.lines.append(line)


def _install_capture_writer(monkeypatch):
    from tracenest import logger as logger_module

    cap = _CaptureWriter()

    def _fake_get_writer():
        return cap

    monkeypatch.setattr(logger_module, "_get_writer", _fake_get_writer)
    return cap


def _build_app():
    app = FastAPI()

    @app.get("/ok")
    def ok():
        return {"status": "ok"}

    @app.get("/fail")
    def fail():
        raise RuntimeError("boom")

    # Excluded path (simulate health/UI)
    excluded = next(iter(FASTAPI_EXCLUDED_PATHS)) if FASTAPI_EXCLUDED_PATHS else "/health"

    @app.get(excluded)
    def health():
        return {"status": "healthy"}

    app.add_middleware(TraceNestMiddleware)
    return app, excluded


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_request_success_is_logged(monkeypatch):
    cap = _install_capture_writer(monkeypatch)
    app, _ = _build_app()
    client = TestClient(app)

    res = client.get("/ok")
    assert res.status_code == 200

    assert len(cap.lines) == 1
    data = json.loads(cap.lines[0])

    assert data["level"] == "INFO"
    assert data["msg"] == "HTTP request completed"
    assert data["meta"]["method"] == "GET"
    assert data["meta"]["path"] == "/ok"
    assert data["meta"]["status_code"] == 200
    assert "duration_ms" in data["meta"]
    assert "trace_id" in data


def test_request_exception_is_logged(monkeypatch):
    cap = _install_capture_writer(monkeypatch)
    app, _ = _build_app()
    client = TestClient(app)

    with pytest.raises(RuntimeError):
        client.get("/fail")

    assert len(cap.lines) == 1
    data = json.loads(cap.lines[0])

    assert data["level"] == "ERROR"
    assert data["msg"] == "HTTP request failed"
    assert data["meta"]["path"] == "/fail"
    assert "exc" in data
    assert "stack" in data["exc"]
    assert "trace_id" in data


def test_excluded_paths_are_not_logged(monkeypatch):
    cap = _install_capture_writer(monkeypatch)
    app, excluded = _build_app()
    client = TestClient(app)

    res = client.get(excluded)
    assert res.status_code == 200

    assert cap.lines == []


def test_trace_id_is_consistent_per_request(monkeypatch):
    cap = _install_capture_writer(monkeypatch)
    app, _ = _build_app()
    client = TestClient(app)

    client.get("/ok")
    client.get("/ok")

    assert len(cap.lines) == 2
    first = json.loads(cap.lines[0])["trace_id"]
    second = json.loads(cap.lines[1])["trace_id"]

    assert first != second
