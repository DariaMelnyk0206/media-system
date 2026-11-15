"""
src/models/topic.py
~~~~~~~~~~~~~~~~~~~~
Pydantic domain models for Topic.

Covers:
  HD-015  Topic has id and name.
  HD-023  Topic may have zero or more MediaItems.
  VR-003  Topic name not empty.
  VR-004  Topic name trimmed.
  VR-005  Topic name unique case-insensitively.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.models.media_item import MediaItemRef

# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------


class CreateTopicRequest(BaseModel):
    """POST /api/topics request body."""

    name: str


class UpdateTopicRequest(BaseModel):
    """PATCH /api/topics/{id} request body."""

    name: str


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class TopicSummary(BaseModel):
    """Lightweight Topic without media_items — used in GET /api/topics list."""

    id: str
    name: str


class Topic(BaseModel):
    """Full Topic domain object including associated MediaItems."""

    id: str
    name: str
    media_items: list[MediaItemRef] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Search result
# ---------------------------------------------------------------------------


class SearchResultItem(BaseModel):
    """Unified search result item with 'kind' discriminator (IR-024, DD-008).

    kind == "media_item": type, status, rating are populated.
    kind == "topic":      type, status, rating are null.
    """

    kind: str
    id: str
    name: str
    type: str | None = None
    status: str | None = None
    rating: int | None = None


# ---------------------------------------------------------------------------
# Typed list/search response wrappers
# Used as response_model in routes so FastAPI exposes the schemas in openapi.json.
# ---------------------------------------------------------------------------


class TopicListResponse(BaseModel):
    """Response body for GET /api/topics."""

    data: list[TopicSummary]


class SearchResponse(BaseModel):
    """Response body for GET /api/search."""

    data: list[SearchResultItem]
