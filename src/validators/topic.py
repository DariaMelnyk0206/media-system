"""
src/validators/topic.py
~~~~~~~~~~~~~~~~~~~~~~~~
Validation rules for Topic fields.

VR-003  Topic name must not be empty after trim
VR-004  Topic name is trimmed before saving
VR-005  Topic name must be unique case-insensitively (create)
VR-006  Topic name must be unique case-insensitively (rename — same rule applied)

(The user spec refers to these as VR-010..011 in the task description;
the api-design-spec.md labels them VR-003..006.  This module implements
the behaviour described either way: non-empty, trimmed, case-insensitively unique.)
"""

from __future__ import annotations

from src.errors import error_codes
from src.errors.handlers import ConflictError, ValidationError
from src.logging.logger import get_logger

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# VR-003 / VR-004  name
# ---------------------------------------------------------------------------


def validate_and_trim_name(name: str) -> str:
    """Trim Topic name and reject if empty after trim (VR-003, VR-004).

    Returns the trimmed name on success.
    Raises ValidationError(NAME_REQUIRED) on failure.
    """
    trimmed = name.strip()
    if not trimmed:
        log.debug("validation.topic.name_required  raw=%r", name)
        raise ValidationError(error_codes.NAME_REQUIRED, field="name")
    return trimmed


# ---------------------------------------------------------------------------
# VR-005 / VR-006  case-insensitive uniqueness
# ---------------------------------------------------------------------------


def check_unique(name: str, existing_topics: dict, exclude_id: str | None = None) -> None:
    """Raise ConflictError if a topic with the same name (case-insensitive) exists.

    Args:
        name:            Already-trimmed name to check.
        existing_topics: Raw dict of { topic_id: {"id": ..., "name": ...} }.
        exclude_id:      Topic id to skip during comparison (used for rename so a
                         topic can keep its own name without triggering a conflict).

    Raises ConflictError(NAME_TAKEN) on duplicate.
    """
    name_lower = name.lower()
    for raw in existing_topics.values():
        if raw["id"] == exclude_id:
            continue
        if raw["name"].lower() == name_lower:
            log.debug(
                "validation.topic.name_taken  name=%r  conflicting_id=%s",
                name,
                raw["id"],
            )
            raise ConflictError(error_codes.NAME_TAKEN, field="name")


# ---------------------------------------------------------------------------
# Convenience: validate full create payload
# ---------------------------------------------------------------------------


def validate_create(name: str, existing_topics: dict) -> str:
    """Run VR-003/004 and VR-005 for a create request.

    Returns trimmed name.
    """
    trimmed = validate_and_trim_name(name)
    check_unique(trimmed, existing_topics)
    return trimmed


# ---------------------------------------------------------------------------
# Convenience: validate rename payload
# ---------------------------------------------------------------------------


def validate_rename(name: str, existing_topics: dict, topic_id: str) -> str:
    """Run VR-003/004 and VR-006 for a rename request.

    exclude_id=topic_id so renaming to the same (identical) name is allowed.
    Returns trimmed name.
    """
    trimmed = validate_and_trim_name(name)
    check_unique(trimmed, existing_topics, exclude_id=topic_id)
    return trimmed
