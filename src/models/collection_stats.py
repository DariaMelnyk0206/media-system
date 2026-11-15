"""Response models for collection-wide statistics."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TopicStatItem(BaseModel):
    """Topic summary with its number of distinct associated MediaItems."""

    id: UUID
    name: str
    media_item_count: int = Field(ge=0)


class StatusCounts(BaseModel):
    """Counts for every supported MediaItem status."""

    model_config = ConfigDict(extra="forbid")

    planned: int = Field(ge=0)
    in_progress: int = Field(ge=0)
    postponed: int = Field(ge=0)
    abandoned: int = Field(ge=0)
    completed: int = Field(ge=0)


class TypeCounts(BaseModel):
    """Counts for every supported MediaItem type."""

    model_config = ConfigDict(extra="forbid")

    book: int = Field(ge=0)
    movie: int = Field(ge=0)
    tv_series: int = Field(ge=0)
    article: int = Field(ge=0)
    podcast: int = Field(ge=0)
    video: int = Field(ge=0)
    other: int = Field(ge=0)


class CollectionStatsResponse(BaseModel):
    """Read-only aggregate response for GET /api/stats."""

    total_media_items: int = Field(ge=0)
    total_topics: int = Field(ge=0)
    status_counts: StatusCounts
    type_counts: TypeCounts
    average_rating: float | None = Field(
        ge=1,
        le=10,
        multiple_of=0.01,
    )
    rated_count: int = Field(ge=0)
    topics_summary: list[TopicStatItem]
