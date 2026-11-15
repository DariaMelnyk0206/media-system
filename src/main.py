"""
src/main.py
~~~~~~~~~~~
Application entry point for the Personal Media Library System.

Creates the FastAPI application instance and attaches a middleware that logs
every inbound HTTP request and its response status to logs/system.log.

No business routes or persistence logic are included at this stage.
Those are added in Phase 3 (FEAT-001..012 per PEP-001).

Run locally:
    uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import time

from fastapi import FastAPI, Request, Response

from src.logging.logger import get_logger

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------

log = get_logger(__name__)

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Personal Media Library System",
    version="0.1.0",
    description=(
        "REST API for the Personal Media Library System (SRS-001 v1.0). "
        "Covers REQ-F-001 through REQ-F-066."
    ),
    # No authentication — CON-008, CON-013, HD-007, HD-046
    openapi_tags=[
        {"name": "MediaItems", "description": "MediaItem CRUD and status management"},
        {"name": "Topics", "description": "Topic CRUD"},
        {"name": "Associations", "description": "MediaItem–Topic associations"},
        {"name": "Search", "description": "Unified search across MediaItems and Topics"},
    ],
)

# ---------------------------------------------------------------------------
# Request / Response logging middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def log_requests(request: Request, call_next: object) -> Response:
    """Log every inbound HTTP request and the resulting response status.

    Logged fields:
        method  — HTTP verb (GET, POST, PATCH, DELETE)
        path    — request path, including query string when present
        status  — HTTP status code of the response
        ms      — processing time in milliseconds

    Example log line:
        2026-11-15 18:05:01,042  INFO      pmls.main  GET /api/media-items → 200 (4ms)

    Both request and response are passed through unmodified.
    """
    start = time.perf_counter()

    # call_next is typed as Callable in the FastAPI type stubs;
    # the actual call is always awaitable at runtime.
    response: Response = await call_next(request)  # type: ignore[operator]

    duration_ms = round((time.perf_counter() - start) * 1000)
    path = request.url.path
    if request.url.query:
        path = f"{path}?{request.url.query}"

    log.info(
        "%s %s → %d (%dms)",
        request.method,
        path,
        response.status_code,
        duration_ms,
    )

    return response


# ---------------------------------------------------------------------------
# Startup / shutdown events
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def on_startup() -> None:
    """Log application startup.

    Repository initialisation (load from data/media_store.json) will be
    added here in FEAT-012 (Phase 3).
    """
    log.info("PMLS application starting up — no routes registered yet (pre-Phase 3)")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Log application shutdown."""
    log.info("PMLS application shutting down")
