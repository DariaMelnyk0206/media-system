"""
src/services/association_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business logic for MediaItem–Topic Many-to-Many associations.

Covers FEAT-006 (REQ-F-030..034) and FEAT-007 navigation.

Associations are stored as a ``topic_ids`` list inside each MediaItem entry.
The Topic side derives its ``media_items`` list at read time by scanning all
MediaItems — no duplicate storage.

Logging events emitted:
  association.link    — topic added to media item (or media item added to topic)
  association.unlink  — topic removed from media item (or vice versa)
"""

from __future__ import annotations

from src.errors.handlers import NotFoundError
from src.logging.logger import get_logger
from src.models.media_item import MediaItem
from src.models.topic import Topic
from src.repository import media_item_repo, storage, topic_repo

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# REQ-F-030  Add Topic to MediaItem  (POST /media-items/{id}/topics/{topicId})
# ---------------------------------------------------------------------------


def add_topic_to_media_item(item_id: str, topic_id: str) -> MediaItem:
    """Associate a Topic with a MediaItem (idempotent, DD-006).

    Raises NotFoundError if either entity does not exist.
    Returns the updated MediaItem.
    """
    if media_item_repo.get_by_id(item_id) is None:
        log.debug("association.link  NOT_FOUND  media_id=%s", item_id)
        raise NotFoundError()
    if topic_repo.get_by_id(topic_id) is None:
        log.debug("association.link  NOT_FOUND  topic_id=%s", topic_id)
        raise NotFoundError()

    item = media_item_repo.add_topic(item_id, topic_id)
    if item is None:
        raise NotFoundError()

    storage.save()
    log.info("association.link  media_id=%s  topic_id=%s", item_id, topic_id)
    return item


# ---------------------------------------------------------------------------
# REQ-F-031  Remove Topic from MediaItem  (DELETE /media-items/{id}/topics/{topicId})
# ---------------------------------------------------------------------------


def remove_topic_from_media_item(item_id: str, topic_id: str) -> None:
    """Remove a Topic association from a MediaItem.

    Raises NotFoundError if the MediaItem is not found, or if the
    association does not exist (AC-054 — no dangling references).
    """
    if media_item_repo.get_by_id(item_id) is None:
        log.debug("association.unlink  NOT_FOUND  media_id=%s", item_id)
        raise NotFoundError()

    result = media_item_repo.remove_topic(item_id, topic_id)
    # result is None  → item not found (already handled above, but guard anyway)
    # result is False → association did not exist → 404
    if result is None or result is False:
        log.debug(
            "association.unlink  NOT_FOUND  media_id=%s  topic_id=%s", item_id, topic_id
        )
        raise NotFoundError()

    storage.save()
    log.info("association.unlink  media_id=%s  topic_id=%s", item_id, topic_id)


# ---------------------------------------------------------------------------
# REQ-F-032  Add MediaItem to Topic  (POST /topics/{id}/media-items/{mediaId})
# ---------------------------------------------------------------------------


def add_media_item_to_topic(topic_id: str, media_id: str) -> Topic:
    """Associate a MediaItem with a Topic (idempotent, DD-006).

    Raises NotFoundError if either entity does not exist.
    Returns the updated Topic.
    """
    if topic_repo.get_by_id(topic_id) is None:
        log.debug("association.link  NOT_FOUND  topic_id=%s", topic_id)
        raise NotFoundError()
    if media_item_repo.get_by_id(media_id) is None:
        log.debug("association.link  NOT_FOUND  media_id=%s", media_id)
        raise NotFoundError()

    topic = topic_repo.add_media_item(topic_id, media_id)
    if topic is None:
        raise NotFoundError()

    storage.save()
    log.info("association.link  topic_id=%s  media_id=%s", topic_id, media_id)
    return topic


# ---------------------------------------------------------------------------
# REQ-F-033  Remove MediaItem from Topic  (DELETE /topics/{id}/media-items/{mediaId})
# ---------------------------------------------------------------------------


def remove_media_item_from_topic(topic_id: str, media_id: str) -> None:
    """Remove a MediaItem association from a Topic.

    Raises NotFoundError if the Topic is not found, or if the
    association does not exist.
    """
    if topic_repo.get_by_id(topic_id) is None:
        log.debug("association.unlink  NOT_FOUND  topic_id=%s", topic_id)
        raise NotFoundError()

    result = topic_repo.remove_media_item(topic_id, media_id)
    # result is None  → topic or media_item not found
    # result is False → association did not exist
    if result is None or result is False:
        log.debug(
            "association.unlink  NOT_FOUND  topic_id=%s  media_id=%s", topic_id, media_id
        )
        raise NotFoundError()

    storage.save()
    log.info("association.unlink  topic_id=%s  media_id=%s", topic_id, media_id)
