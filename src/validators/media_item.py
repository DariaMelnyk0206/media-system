"""
src/validators/media_item.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validation rules VR-001..009 for MediaItem fields.

Each function raises ValidationError on violation.
Callers (service layer) invoke these before any repository write.

VR-001  name after trim must not be empty
VR-002  name is trimmed before saving
VR-007  rating when present must be integer 1-10
VR-008  type must be one of 7 valid MediaType values  (enforced by Pydantic enum)
VR-009  status must be one of 5 valid MediaStatus values (enforced by Pydantic enum)
"""

from __future__ import annotations

from src.errors import error_codes
from src.errors.handlers import ValidationError
from src.logging.logger import get_logger
from src.validators.common import validate_name

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# VR-001 / VR-002  name
# ---------------------------------------------------------------------------


def validate_and_trim_name(name: str) -> str:
    """Trim name and reject if empty after trim (VR-001, VR-002).

    Returns the trimmed name on success.
    Raises ValidationError(NAME_REQUIRED) on failure.
    """
    return validate_name(name, logger=log, event="validation.name_required ")


# ---------------------------------------------------------------------------
# VR-007  rating
# ---------------------------------------------------------------------------


def validate_rating(rating: int | None) -> None:
    """Reject rating outside [1, 10] when provided (VR-007).

    None is always accepted (unset rating).
    Raises ValidationError(RATING_OUT_OF_RANGE) on failure.
    """
    if rating is None:
        return
    if not isinstance(rating, int) or rating < 1 or rating > 10:
        log.debug("validation.rating_out_of_range  rating=%r", rating)
        raise ValidationError(error_codes.RATING_OUT_OF_RANGE, field="rating")


def validate_rating_bounds(
    rating_min: int | None,
    rating_max: int | None,
) -> None:
    """Validate list-query rating bounds (VR-010, VR-011)."""
    if rating_min is not None and not 1 <= rating_min <= 10:
        raise ValidationError(error_codes.INVALID_RATING_BOUND, field="rating_min")
    if rating_max is not None and not 1 <= rating_max <= 10:
        raise ValidationError(error_codes.INVALID_RATING_BOUND, field="rating_max")
    if rating_min is not None and rating_max is not None and rating_min > rating_max:
        raise ValidationError(error_codes.INVALID_RATING_RANGE, field="rating_min")


# ---------------------------------------------------------------------------
# Convenience: validate full create payload
# ---------------------------------------------------------------------------


def validate_create(name: str, rating: int | None) -> str:
    """Run VR-001/002 and VR-007 for a create request.

    Returns trimmed name.
    VR-008 and VR-009 are handled by Pydantic enum parsing upstream.
    """
    trimmed = validate_and_trim_name(name)
    validate_rating(rating)
    return trimmed


# ---------------------------------------------------------------------------
# Convenience: validate update payload (only provided fields)
# ---------------------------------------------------------------------------


def validate_update(name: str | None, rating: int | None, set_fields: set[str]) -> str | None:
    """Run applicable VRs for a PATCH request.

    Returns trimmed name if 'name' is in set_fields, else None.
    """
    trimmed_name: str | None = None
    if "name" in set_fields and name is not None:
        trimmed_name = validate_and_trim_name(name)
    if "rating" in set_fields:
        validate_rating(rating)
    return trimmed_name
