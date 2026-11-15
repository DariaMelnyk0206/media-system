"""
src/repository/topic_repo.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In-memory CRUD repository for Topic.

Internal storage format per entry:
  {
    "id":   str (UUID),
    "name": str (trimmed, unique case-insensitively)
  }

MediaItem associations are stored on the MediaItem side (topic_ids list).
The list of media_items in a Topic response is derived by scanning all
media_item entries for matching topic_ids.
"""

from __future__ import annotations

import uuid
from typing import Optional

from src.logging.logger import get_logger
from src.models.media_item import MediaItemRef, MediaStatus, MediaType
from src.models.topic import Topic, TopicSummary
from src.repository import storage

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _derive_media_items(topic_id: str) -> list[MediaItemRef]:
    """Collect all MediaItems whose topic_ids list contains topic_id."""
    result = []
    for raw in storage.get_media_items().values():
        if topic_id in raw.get("topic_ids", []):
            result.append(
                MediaItemRef(
                    id=raw["id"],
                    name=raw["name"],
                    type=MediaType(raw["type"]),
                    status=MediaStatus(raw["status"]),
                    rating=raw.get("rating"),
                )
            )
    return result


def _to_model(raw: dict) -> Topic:
    return Topic(
        id=raw["id"],
        name=raw["name"],
        media_items=_derive_media_items(raw["id"]),
    )


def _to_summary(raw: dict) -> TopicSummary:
    return TopicSummary(id=raw["id"], name=raw["name"])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create(name: str) -> Topic:
    """Insert a new Topic and return it."""
    topics = storage.get_topics()
    topic_id = str(uuid.uuid4())
    raw = {"id": topic_id, "name": name}
    topics[topic_id] = raw
    log.info("topic.create  id=%s  name=%r", topic_id, name)
    return _to_model(raw)


def get_by_id(topic_id: str) -> Optional[Topic]:
    topics = storage.get_topics()
    raw = topics.get(topic_id)
    return _to_model(raw) if raw else None


def list_all() -> list[TopicSummary]:
    return [_to_summary(raw) for raw in storage.get_topics().values()]


def find_by_name_ci(name: str) -> Optional[dict]:
    """Return raw dict of the topic whose name matches case-insensitively, or None."""
    normalised = name.strip().lower()
    for raw in storage.get_topics().values():
        if raw["name"].lower() == normalised:
            return raw
    return None


def rename(topic_id: str, new_name: str) -> Optional[Topic]:
    """Rename a Topic.  Returns updated Topic, or None if not found."""
    topics = storage.get_topics()
    raw = topics.get(topic_id)
    if raw is None:
        return None
    old_name = raw["name"]
    raw["name"] = new_name
    log.info("topic.rename  id=%s  old=%r  new=%r", topic_id, old_name, new_name)
    return _to_model(raw)


def delete(topic_id: str) -> bool:
    """Delete a Topic and remove it from all MediaItem topic_ids."""
    topics = storage.get_topics()
    if topic_id not in topics:
        return False
    name = topics[topic_id]["name"]
    del topics[topic_id]

    # Remove reference from all media items
    for raw in storage.get_media_items().values():
        if topic_id in raw.get("topic_ids", []):
            raw["topic_ids"].remove(topic_id)

    log.info("topic.delete  id=%s  name=%r", topic_id, name)
    return True


# ---------------------------------------------------------------------------
# Association helpers
# ---------------------------------------------------------------------------


def add_media_item(topic_id: str, media_item_id: str) -> Optional[Topic]:
    """Add media_item_id to the topic's association (via media_item side)."""
    topics = storage.get_topics()
    if topic_id not in topics:
        return None
    items = storage.get_media_items()
    if media_item_id not in items:
        return None
    raw_item = items[media_item_id]
    if topic_id not in raw_item.get("topic_ids", []):
        raw_item.setdefault("topic_ids", []).append(topic_id)
        log.info("topic.add_media_item  topic_id=%s  media_id=%s", topic_id, media_item_id)
    return _to_model(topics[topic_id])


def remove_media_item(topic_id: str, media_item_id: str) -> Optional[bool]:
    """Remove media_item_id from topic's association.

    Returns True (removed), False (not associated), None (topic not found).
    """
    topics = storage.get_topics()
    if topic_id not in topics:
        return None
    items = storage.get_media_items()
    raw_item = items.get(media_item_id)
    if raw_item is None:
        return None
    if topic_id not in raw_item.get("topic_ids", []):
        return False
    raw_item["topic_ids"].remove(topic_id)
    log.info("topic.remove_media_item  topic_id=%s  media_id=%s", topic_id, media_item_id)
    return True
