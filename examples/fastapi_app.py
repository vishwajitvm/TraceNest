from fastapi import FastAPI

from tracenest import logger
from tracenest.fastapi.middleware import TraceNestMiddleware
from tracenest.ui.router import router as tracenest_router

app = FastAPI()

# Attach TraceNest
app.add_middleware(TraceNestMiddleware)
app.include_router(tracenest_router)


@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"ok": True}
