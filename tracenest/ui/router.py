from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

router = APIRouter()

BASE = Path(__file__).parent
TEMPLATES = BASE / "templates"
STATIC = BASE / "static"

router.mount(
    "/tracenest/static",
    StaticFiles(directory=STATIC),
    name="tracenest-static",
)

@router.get("/tracenest", response_class=HTMLResponse)
def ui():
    return (TEMPLATES / "index.html").read_text(encoding="utf-8")
