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
CHANGELOGS_DIR = BASE_DIR / "changelogs"

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
    from ..security.redaction import redact_string
    path = LOG_DIR / filename
    if not path.exists() or not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-limit:]
            return [redact_string(line) for line in lines]
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


@router.get("/api/changelogs")
def list_changelogs():
    try:
        if not CHANGELOGS_DIR.exists():
            return JSONResponse({"versions": []})
        versions = [f.stem for f in CHANGELOGS_DIR.iterdir() if f.is_file() and f.suffix == ".md"]
        # Sort versions properly (e.g. v0.1.6 > v0.1.5)
        versions.sort(key=lambda x: [int(p) if p.isdigit() else p for p in x.replace('v', '').split('.')], reverse=True)
        return JSONResponse({"versions": versions})
    except Exception:
        return JSONResponse({"versions": []})


@router.get("/api/changelogs/{version}")
def get_changelog(version: str):
    path = CHANGELOGS_DIR / f"{version}.md"
    if not path.exists() or not path.is_file():
        return JSONResponse({"error": "Version not found"}, status_code=404)
    
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        return JSONResponse({"version": version, "content": content})
    except Exception:
        return JSONResponse({"error": "Failed to read version"}, status_code=500)


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
