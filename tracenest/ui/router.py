from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

# ─────────────────────────────────────────────
# Paths (STRICTLY MATCH PROJECT STRUCTURE)
# ─────────────────────────────────────────────

BASE_DIR = Path.cwd()
LOG_DIR = BASE_DIR / "TraceNestLogs"

UI_DIR = Path(__file__).parent
TEMPLATES_DIR = UI_DIR / "templates"

# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────

router = APIRouter(prefix="/tracenest", tags=["TraceNest UI"])


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
        return sorted(
            [f.name for f in LOG_DIR.iterdir() if f.is_file() and f.suffix == ".log"],
            reverse=True,
        )
    except Exception:
        return []


def _read_log_file(filename: str, limit: int = 500) -> List[str]:
    path = LOG_DIR / filename
    if not path.exists() or not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()[-limit:]
    except Exception:
        return []


# ─────────────────────────────────────────────
# UI ROUTES (FILES SERVED EXPLICITLY)
# ─────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def tracenest_ui(request: Request):
    """
    Main TraceNest UI entry point.
    """
    try:
        return (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")
    except Exception:
        return "<h1>TraceNest UI failed to load</h1>"


@router.get("/app.js")
def tracenest_app_js():
    return FileResponse(
        TEMPLATES_DIR / "app.js",
        media_type="application/javascript",
    )


@router.get("/styles.css")
def tracenest_styles_css():
    return FileResponse(
        TEMPLATES_DIR / "styles.css",
        media_type="text/css",
    )


# ─────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────

@router.get("/api/logs")
def list_logs():
    return JSONResponse({"logs": _list_log_files()})


@router.get("/api/logs/{filename}")
def get_log_file(filename: str, limit: int = 500):
    return JSONResponse(
        {
            "file": filename,
            "lines": _read_log_file(filename, limit),
        }
    )
