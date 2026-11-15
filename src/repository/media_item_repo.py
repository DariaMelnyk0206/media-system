"""
src/repository/media_item_repo.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In-memory CRUD repository for MediaItem.

All operations work against the dict returned by storage.get_media_items().
Persistence is triggered by the caller (service layer) after each mutation.

Internal storage format per entry:
  {
    "id":        str (UUID),
    "name":      str,
    "type":      str (MediaType value),
    "status":    str (MediaStatus value),
    "notes":     str | null,
    "rating":    int | null,
    "topic_ids": list[str]   ← UUIDs of associated Topics
  }
"""

from __future__ import annotations

import uuid

from src.logging.logger import get_logger
from src.models.media_item import (
    CreateMediaItemRequest,
    MediaItem,
    MediaStatus,
    MediaType,
    TopicRef,
    UpdateMediaItemRequest,
)
from src.repository import storage

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_model(raw: dict, topic_map: dict[str, dict]) -> MediaItem:
    """Convert a raw storage dict to a MediaItem Pydantic model.

    topic_map: { topic_id: {"id":..., "name":...} } — used to build TopicRef list.
    """
    topic_refs = [
        TopicRef(id=tid, name=topic_map[tid]["name"])
        for tid in raw.get("topic_ids", [])
        if tid in topic_map
    ]
    return MediaItem(
        id=raw["id"],
        name=raw["name"],
        type=MediaType(raw["type"]),
        status=MediaStatus(raw["status"]),
        notes=raw.get("notes"),
        rating=raw.get("rating"),
        topics=topic_refs,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def create(req: CreateMediaItemRequest) -> MediaItem:
    """Insert a new MediaItem into the store and return the created model."""
    store = storage.get_media_items()
    topics = storage.get_topics()

    item_id = str(uuid.uuid4())
    raw: dict = {
        "id": item_id,
        "name": req.name,
        "type": req.type.value,
        "status": req.status.value,
        "notes": req.notes,
        "rating": req.rating,
        "topic_ids": [tid for tid in req.topic_ids if tid in topics],
    }
    store[item_id] = raw
    log.info("media_item.create  id=%s  name=%r  type=%s", item_id, req.name, req.type.value)
    return _to_model(raw, topics)


def get_by_id(item_id: str) -> MediaItem | None:
    """Return the MediaItem with the given id, or None if not found."""
    store = storage.get_media_items()
    raw = store.get(item_id)
    if raw is None:
        return None
    return _to_model(raw, storage.get_topics())


def list_all() -> list[MediaItem]:
    """Return all MediaItems as a list."""
    topics = storage.get_topics()
    return [_to_model(raw, topics) for raw in storage.get_media_items().values()]


def update(item_id: str, req: UpdateMediaItemRequest, set_fields: set[str]) -> MediaItem | None:
    """Apply a partial update.  Only fields present in set_fields are written.

    set_fields is model_fields_set from the parsed request body — it correctly
    includes fields explicitly set to None, distinguishing them from absent fields.
    """
    store = storage.get_media_items()
    raw = store.get(item_id)
    if raw is None:
        return None

    if "name" in set_fields and req.name is not None:
        raw["name"] = req.name
    if "type" in set_fields and req.type is not None:
        raw["type"] = req.type.value
    if "status" in set_fields and req.status is not None:
        raw["status"] = req.status.value
    if "notes" in set_fields:
        raw["notes"] = req.notes  # allow None (clear)
    if "rating" in set_fields:
        raw["rating"] = req.rating  # allow None (clear)

    log.info("media_item.update  id=%s  fields=%s", item_id, set_fields)
    return _to_model(raw, storage.get_topics())


def delete(item_id: str) -> bool:
    """Remove a MediaItem.  Returns True if deleted, False if not found."""
    store = storage.get_media_items()
    if item_id not in store:
        return False
    name = store[item_id].get("name", "")
    del store[item_id]

    # Remove association from all topics
    for t_raw in storage.get_topics().values():
        t_raw.setdefault("media_item_ids", [])
        if item_id in t_raw.get("media_item_ids", []):
            t_raw["media_item_ids"].remove(item_id)

    log.info("media_item.delete  id=%s  name=%r", item_id, name)
    return True


# ---------------------------------------------------------------------------
# Association helpers (called by association routes)
# ---------------------------------------------------------------------------


def add_topic(item_id: str, topic_id: str) -> MediaItem | None:
    """Add topic_id to the item's topic_ids if not already present."""
    store = storage.get_media_items()
    raw = store.get(item_id)
    if raw is None:
        return None
    if topic_id not in raw["topic_ids"]:
        raw["topic_ids"].append(topic_id)
        log.info("media_item.add_topic  item_id=%s  topic_id=%s", item_id, topic_id)
    return _to_model(raw, storage.get_topics())


def remove_topic(item_id: str, topic_id: str) -> bool | None:
    """Remove topic_id from item's topic_ids.

    Returns:
        True  — removed successfully
        False — association did not exist
        None  — MediaItem not found
    """
    store = storage.get_media_items()
    raw = store.get(item_id)
    if raw is None:
        return None
    if topic_id not in raw["topic_ids"]:
        return False
    raw["topic_ids"].remove(topic_id)
    log.info("media_item.remove_topic  item_id=%s  topic_id=%s", item_id, topic_id)
    return True
