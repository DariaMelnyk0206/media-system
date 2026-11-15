"""Read-only aggregation service for collection statistics."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from src.errors.handlers import StatisticsFailedError
from src.logging.logger import get_logger
from src.models.collection_stats import (
    CollectionStatsResponse,
    StatusCounts,
    TopicStatItem,
    TypeCounts,
)
from src.models.media_item import MediaStatus, MediaType
from src.repository import media_item_repo, topic_repo

log = get_logger(__name__)


def get_collection_stats() -> CollectionStatsResponse:
    """Calculate current collection aggregates without changing stored data.

    Topic counts are derived from each MediaItem's associations. Each MediaItem
    contributes at most once to any particular Topic's count.
    """
    try:
        media_items = media_item_repo.list_all()
        topics = topic_repo.list_all()

        status_counts = {status.value: 0 for status in MediaStatus}
        type_counts = {media_type.value: 0 for media_type in MediaType}
        rated_total = 0
        rated_count = 0
        topic_counts = {topic.id: 0 for topic in topics}

        for item in media_items:
            status_counts[item.status.value] += 1
            type_counts[item.type.value] += 1
            if item.rating is not None:
                rated_total += item.rating
                rated_count += 1
            for topic_id in {topic.id for topic in item.topics}:
                if topic_id in topic_counts:
                    topic_counts[topic_id] += 1

        average_rating = None
        if rated_count:
            average_rating = float(
                (Decimal(rated_total) / Decimal(rated_count)).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )
            )

        topics_summary = sorted(
            (
                TopicStatItem(
                    id=topic.id,
                    name=topic.name,
                    media_item_count=topic_counts[topic.id],
                )
                for topic in topics
            ),
            key=lambda topic: (-topic.media_item_count, topic.name.casefold()),
        )
        result = CollectionStatsResponse(
            total_media_items=len(media_items),
            total_topics=len(topics),
            status_counts=StatusCounts(**status_counts),
            type_counts=TypeCounts(**type_counts),
            average_rating=average_rating,
            rated_count=rated_count,
            topics_summary=topics_summary,
        )
    except Exception as exc:
        log.error("stats.query  status=500  error_type=%s", type(exc).__name__)
        raise StatisticsFailedError() from exc

    log.info(
        "stats.query  status=200  total_media_items=%d  total_topics=%d  rated_count=%d",
        result.total_media_items,
        result.total_topics,
        result.rated_count,
    )
    return result
