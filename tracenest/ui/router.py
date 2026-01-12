"""
TraceNest UI Router

Provides a read-only UI for inspecting TraceNest logs.

SAFETY GUARANTEES:
- Read-only access
- Never raises exceptions outward
- Never blocks application execution
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse

from ..core.config import (
    UI_ROUTE_PATH,
    LOG_FILE_EXTENSION,
)
from ..core.config import get_log_root_path

router = APIRouter()


# =====================================================================
# UI Page
# =====================================================================


@router.get(UI_ROUTE_PATH, response_class=HTMLResponse)
def tracenest_ui() -> str:
    """
    Serves the main TraceNest UI page.
    """
    return """
    <html>
      <head>
        <title>TraceNest Logs</title>
        <style>
          body { font-family: monospace; background: #111; color: #eee; }
          a { color: #7dbfff; text-decoration: none; }
          pre { white-space: pre-wrap; }
        </style>
      </head>
      <body>
        <h2>TraceNest Logs</h2>
        <ul id="files"></ul>
        <pre id="log"></pre>

        <script>
          async function loadFiles() {
            const res = await fetch('/tracenest/files');
            const files = await res.json();
            const ul = document.getElementById('files');
            ul.innerHTML = '';
            files.forEach(f => {
              const li = document.createElement('li');
              const a = document.createElement('a');
              a.href = '#';
              a.innerText = f;
              a.onclick = () => loadLog(f);
              li.appendChild(a);
              ul.appendChild(li);
            });
          }

          async function loadLog(file) {
            const res = await fetch('/tracenest/logs/' + file);
            const text = await res.text();
            document.getElementById('log').innerText = text;
          }

          loadFiles();
        </script>
      </body>
    </html>
    """


# =====================================================================
# API Endpoints
# =====================================================================


@router.get(f"{UI_ROUTE_PATH}/files")
def list_log_files() -> List[str]:
    """
    Lists available log files.
    """
    log_root = get_log_root_path()
    if not log_root.exists():
        return []

    files = []
    for item in log_root.iterdir():
        if item.is_file() and item.name.endswith(LOG_FILE_EXTENSION):
            files.append(item.name)

    return sorted(files)


@router.get(f"{UI_ROUTE_PATH}/logs/{{filename}}", response_class=PlainTextResponse)
def read_log_file(filename: str) -> str:
    """
    Reads a specific log file safely.
    """
    if not filename.endswith(LOG_FILE_EXTENSION):
        raise HTTPException(status_code=400, detail="Invalid file")

    log_root = get_log_root_path()
    file_path = log_root / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Log file not found")

    try:
        return file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to read log file")
