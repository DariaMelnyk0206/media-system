"""
src/errors/responses.py
~~~~~~~~~~~~~~~~~~~~~~~~
Shared FastAPI ``responses`` dicts for route decorators.

Both ``src/routes/media_items.py`` and ``src/routes/topics.py`` need the same
set of additional-response declarations to align the generated OpenAPI schema
with ``docs/openapi.yaml``.  Defining them once here eliminates the duplication.

Usage::

    from src.errors.responses import err400, err404, err409, err500

    @router.post("", responses={400: err400, 404: err404, 500: err500})
    def create_item(...): ...
"""

from __future__ import annotations

from src.errors.error_codes import ErrorResponse

#: 400 Bad Request — validation rule violated.
err400: dict = {"model": ErrorResponse, "description": "Validation error"}

#: 404 Not Found — resource does not exist.
err404: dict = {"model": ErrorResponse, "description": "Not found"}

#: 409 Conflict — e.g. duplicate Topic name.
err409: dict = {"model": ErrorResponse, "description": "Conflict"}

#: 500 Internal Server Error — auto-save failed (REQ-F-060).
err500: dict = {"model": ErrorResponse, "description": "Auto-save failed"}
