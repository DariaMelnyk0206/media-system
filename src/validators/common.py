"""Shared validation helpers."""

from __future__ import annotations

from logging import Logger

from src.errors.error_codes import NAME_REQUIRED
from src.errors.handlers import ValidationError


def validate_name(name: str, *, logger: Logger, event: str) -> str:
    """Trim a required name and raise the established validation error if empty."""
    trimmed = name.strip()
    if not trimmed:
        logger.debug("%s raw=%r", event, name)
        raise ValidationError(NAME_REQUIRED, field="name")
    return trimmed
