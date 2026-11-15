"""
src/main.py
~~~~~~~~~~~
Application entry point for the Personal Media Library System.

Run locally:
    uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.errors.handlers import (
    PMSLHTTPException,
    http_exception_handler,
    pmls_exception_handler,
    validation_exception_handler,
)
from src.logging.logger import get_logger
from src.repository import storage
from src.routes.media_items import assoc_router as media_assoc_router
from src.routes.media_items import router as media_items_router
from src.routes.search import router as search_router
from src.routes.topics import assoc_router as topic_assoc_router
from src.routes.topics import router as topics_router

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("PMLS starting up — loading store")
    storage.load()
    log.info("PMLS startup complete")
    yield
    log.info("PMLS shutting down")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Personal Media Library System",
    version="0.1.0",
    description=(
        "REST API for the Personal Media Library System (SRS-001 v1.0). "
        "Covers REQ-F-001 through REQ-F-066."
    ),
    openapi_tags=[
        {"name": "MediaItems", "description": "MediaItem CRUD and status management"},
        {"name": "MediaItemAssociations", "description": "MediaItem–Topic associations"},
        {"name": "Topics", "description": "Topic CRUD"},
        {"name": "TopicAssociations", "description": "Topic–MediaItem associations"},
        {"name": "Search", "description": "Unified search across MediaItems and Topics"},
    ],
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

app.add_exception_handler(PMSLHTTPException, pmls_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(media_items_router, prefix="/api")
app.include_router(media_assoc_router, prefix="/api")
app.include_router(topics_router, prefix="/api")
app.include_router(topic_assoc_router, prefix="/api")
app.include_router(search_router, prefix="/api")

# ---------------------------------------------------------------------------
# Logging middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000)
    path = request.url.path
    if request.url.query:
        path = f"{path}?{request.url.query}"
    log.info("%s %s → %d (%dms)", request.method, path, response.status_code, duration_ms)
    return response
