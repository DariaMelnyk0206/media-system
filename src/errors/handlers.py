"""
src/errors/handlers.py
~~~~~~~~~~~~~~~~~~~~~~~
Custom HTTP exceptions and FastAPI exception handlers.

All exceptions carry the full ErrorResponse payload so the response body
always contains {error, field, message} — never FastAPI's default
{"detail": "..."} format.

Usage (raising):
    raise ValidationError(error_codes.NAME_REQUIRED, field="name")
    raise NotFoundError()
    raise ConflictError(error_codes.NAME_TAKEN, field="name")
    raise SaveFailedError()
"""

from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.errors.error_codes import (
    INVALID_STATUS,
    INVALID_TYPE,
    MESSAGES,
    NOT_FOUND,
    SAVE_FAILED,
    ErrorResponse,
)

# ---------------------------------------------------------------------------
# Custom exception classes
# ---------------------------------------------------------------------------


class PMSLHTTPException(Exception):
    """Base class for all PMLS domain exceptions."""

    status_code: int
    error: str
    field: str | None
    message: str

    def __init__(
        self,
        error: str,
        *,
        field: str | None = None,
        message: str | None = None,
        status_code: int,
    ) -> None:
        self.error = error
        self.field = field
        self.message = message or MESSAGES.get(error, error)
        self.status_code = status_code
        super().__init__(self.message)

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(error=self.error, field=self.field, message=self.message)


class ValidationError(PMSLHTTPException):
    """400 Bad Request — validation rule violated."""

    def __init__(self, error: str, *, field: str | None = None, message: str | None = None) -> None:
        super().__init__(error, field=field, message=message, status_code=400)


class NotFoundError(PMSLHTTPException):
    """404 Not Found."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(NOT_FOUND, field=None, message=message, status_code=404)


class ConflictError(PMSLHTTPException):
    """409 Conflict."""

    def __init__(self, error: str, *, field: str | None = None, message: str | None = None) -> None:
        super().__init__(error, field=field, message=message, status_code=409)


class SaveFailedError(PMSLHTTPException):
    """500 Internal Server Error — auto-save failure (REQ-F-060)."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(SAVE_FAILED, field=None, message=message, status_code=500)


# ---------------------------------------------------------------------------
# FastAPI exception handlers
# ---------------------------------------------------------------------------


async def pmls_exception_handler(request: Request, exc: PMSLHTTPException) -> JSONResponse:
    """Handle all PMLS domain exceptions → structured ErrorResponse."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_response().model_dump(),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Override FastAPI's default HTTP exception handler.

    Converts Starlette's {"detail": "..."} into our ErrorResponse format.
    404 from an unregistered route is converted to not_found.
    """
    if exc.status_code == 404:
        body = ErrorResponse(error=NOT_FOUND, field=None, message=MESSAGES[NOT_FOUND])
    else:
        body = ErrorResponse(
            error="http_error",
            field=None,
            message=str(exc.detail) if exc.detail else "An unexpected error occurred.",
        )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())



async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Convert Pydantic 422 RequestValidationError into our 400 ErrorResponse.

    Maps enum validation failures for 'type' and 'status' fields to the
    correct machine-readable error codes (VR-008, VR-009).
    """
    errors = exc.errors()
    # Pick the first error to build a single ErrorResponse
    first = errors[0] if errors else {}
    loc = first.get("loc", ())
    field = loc[-1] if loc else None
    err_type = first.get("type", "")

    # Map field name to error code
    if field == "type" and "enum" in err_type:
        error_code = INVALID_TYPE
    elif field == "status" and "enum" in err_type:
        error_code = INVALID_STATUS
    else:
        error_code = "validation_error"

    body = ErrorResponse(
        error=error_code,
        field=str(field) if field is not None else None,
        message=MESSAGES.get(error_code, first.get("msg", "Validation error.")),
    )
    return JSONResponse(status_code=400, content=body.model_dump())
