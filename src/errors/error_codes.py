"""
src/errors/error_codes.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
Machine-readable error codes and the unified ErrorResponse schema.

Source: docs/api-design-spec.md §3
        docs/openapi.yaml  components/schemas/ErrorResponse

ErrorResponse fields (all 3 required by contract):
  error    — machine-readable code (string)
  field    — name of the offending field, or null for non-field errors
  message  — human-readable English message
"""

from __future__ import annotations

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# ErrorResponse schema
# ---------------------------------------------------------------------------


class ErrorResponse(BaseModel):
    """Unified error response body (api-design-spec §3).

    Returned for all 4xx and 5xx responses.
    """

    error: str
    field: str | None = None
    message: str


# ---------------------------------------------------------------------------
# Error code constants
# ---------------------------------------------------------------------------

# 400 — Validation errors
NAME_REQUIRED = "name_required"
RATING_OUT_OF_RANGE = "rating_out_of_range"
INVALID_TYPE = "invalid_type"
INVALID_STATUS = "invalid_status"
INVALID_RATING_RANGE = "invalid_rating_range"
INVALID_RATING_BOUND = "invalid_rating_bound"

# 404
NOT_FOUND = "not_found"

# 409
NAME_TAKEN = "name_taken"

# 500
SAVE_FAILED = "save_failed"


# ---------------------------------------------------------------------------
# Canonical error messages (English, REQ-NF-010)
# ---------------------------------------------------------------------------

MESSAGES: dict[str, str] = {
    NAME_REQUIRED: "Name must not be empty.",
    RATING_OUT_OF_RANGE: "Rating must be between 1 and 10.",
    INVALID_TYPE: "Invalid media type.",
    INVALID_STATUS: "Invalid status value.",
    INVALID_RATING_RANGE: "Lower bound must not exceed upper bound.",
    INVALID_RATING_BOUND: "Rating bound must be between 1 and 10.",
    NOT_FOUND: "Resource not found.",
    NAME_TAKEN: "Topic name is already in use.",
    SAVE_FAILED: "Auto-save failed. Your change is available for this session.",
}
