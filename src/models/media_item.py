"""
src/models/media_item.py
~~~~~~~~~~~~~~~~~~~~~~~~~
Pydantic domain models for MediaItem.

Covers:
  CON-001  7 MediaType values
  CON-002  5 MediaStatus values
  CON-004  Exact field set: id, name, type, status, notes, rating, topics
  CON-005  No temporal metadata fields
  VR-008   type must be one of 7 values
  VR-009   status must be one of 5 values
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class MediaType(str, Enum):
    book = "book"
    movie = "movie"
    tv_series = "tv_series"
    article = "article"
    podcast = "podcast"
    video = "video"
    other = "other"


class MediaStatus(str, Enum):
    planned = "planned"
    in_progress = "in_progress"
    postponed = "postponed"
    abandoned = "abandoned"
    completed = "completed"


# ---------------------------------------------------------------------------
# Lightweight reference — embedded inside Topic responses
# ---------------------------------------------------------------------------


class MediaItemRef(BaseModel):
    """Lightweight MediaItem embedded inside a Topic response (MediaItemRef schema)."""

    id: str
    name: str
    type: MediaType
    status: MediaStatus
    rating: int | None = None


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------


class CreateMediaItemRequest(BaseModel):
    """POST /api/media-items request body."""

    name: str
    type: MediaType
    status: MediaStatus = MediaStatus.planned
    notes: str | None = None
    rating: int | None = None
    topic_ids: list[str] = Field(default_factory=list)


class UpdateMediaItemRequest(BaseModel):
    """PATCH /api/media-items/{id} request body.

    All fields are optional — absent field means no change (DD-004).
    Pass null for notes or rating to clear those fields (DD-005).
    """

    name: str | None = None
    type: MediaType | None = None
    status: MediaStatus | None = None
    notes: str | None = None
    rating: int | None = None
    # Sentinel to distinguish "absent" from "null" for nullable fields.
    # We use a model_fields_set check at the service layer instead.


# ---------------------------------------------------------------------------
# Full domain object — returned by all endpoints
# ---------------------------------------------------------------------------


class TopicRef(BaseModel):
    """Lightweight Topic reference embedded inside MediaItem."""

    id: str
    name: str


class MediaItem(BaseModel):
    """Full MediaItem domain object (CON-004, HD-011)."""

    id: str
    name: str
    type: MediaType
    status: MediaStatus
    notes: str | None = None
    rating: int | None = None
    topics: list[TopicRef] = Field(default_factory=list)
