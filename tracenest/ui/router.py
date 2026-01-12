from __future__ import annotations

import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ─────────────────────────────────────────────
# Constants (internal, no user config)
# ─────────────────────────────────────────────

BASE_DIR = Path.cwd()
LOG_DIR = BASE_DIR / "TraceNestLogs"

UI_DIR = Path(__file__).parent
TEMPLATES_DIR = UI_DIR / "templates"
STATIC_DIR = UI_DIR / "static"

# ─────────────────────────────────────────────
# Router & Templates
# ─────────────────────────────────────────────

router = APIRouter(prefix="/tracenest", tags=["TraceNest UI"])

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ─────────────────────────────────────────────
# Static Assets
# ─────────────────────────────────────────────

router.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="tracenest-static",
)


# ─────────────────────────────────────────────
# Helpers (safe, defensive)
# ─────────────────────────────────────────────

def _ensure_log_dir() -> None:
    try:
        LOG_DIR.mkdir(exist_ok=True)
    except Exception:
        pass


def _list_log_files() -> List[str]:
    _ensure_log_dir()

    try:
        files = [
            f.name
            for f in LOG_DIR.iterdir()
            if f.is_file() and f.suffix == ".log"
        ]
        return sorted(files, reverse=True)
    except Exception:
        return []


def _read_log_file(filename: str, limit: int = 500) -> List[str]:
    path = LOG_DIR / filename

    if not path.exists() or not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            return lines[-limit:]
    except Exception:
        return []


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
async def tracenest_ui(request: Request):
    """
    Main TraceNest UI entry point.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@router.get("/api/logs")
async def list_logs():
    """
    Returns available log files.
    """
    return JSONResponse(
        {
            "logs": _list_log_files(),
        }
    )


@router.get("/api/logs/{filename}")
async def get_log_file(filename: str, limit: int = 500):
    """
    Returns last N lines of a log file.
    """
    lines = _read_log_file(filename, limit)

    return JSONResponse(
        {
            "file": filename,
            "lines": lines,
        }
    )
