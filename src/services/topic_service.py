"""
src/services/topic_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business logic for Topic CRUD operations.

Covers FEAT-005 (Topic CRUD) REQ-F-020..029.

Each method:
  1. Validates input (via src/validators/topic.py)
  2. Delegates to repository for data access
  3. Calls storage.save() after every mutation
  4. Raises domain exceptions (ValidationError, ConflictError, NotFoundError,
     SaveFailedError) so the route layer only needs to call the service.

Logging events emitted:
  topic.create
  topic.update
  topic.delete
"""

from __future__ import annotations

from src.errors.handlers import NotFoundError
from src.logging.logger import get_logger
from src.models.topic import Topic, TopicSummary
from src.repository import storage, topic_repo
from src.validators import topic as topic_validator

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# REQ-F-020..021  Create
# ---------------------------------------------------------------------------


def create_topic(name: str) -> Topic:
    """Validate, create in-memory, save to disk.

    VR-003/004  name trimmed and non-empty
    VR-005      name unique case-insensitively
    REQ-F-059   auto-save after creation
    """
    trimmed = topic_validator.validate_create(name, storage.get_topics())
    topic = topic_repo.create(trimmed)
    storage.save()   # REQ-F-059 — may raise SaveFailedError → 500
    log.info("topic.create  id=%s  name=%r", topic.id, trimmed)
    return topic


# ---------------------------------------------------------------------------
# REQ-F-022  View
# ---------------------------------------------------------------------------


def list_topics() -> list[TopicSummary]:
    """Return all Topics as lightweight summaries."""
    return topic_repo.list_all()


def get_topic(topic_id: str) -> Topic:
    """Return a single Topic or raise NotFoundError."""
    topic = topic_repo.get_by_id(topic_id)
    if topic is None:
        log.debug("topic.get  NOT_FOUND  id=%s", topic_id)
        raise NotFoundError()
    return topic


# ---------------------------------------------------------------------------
# REQ-F-023..025  Edit (PATCH / rename)
# ---------------------------------------------------------------------------


def update_topic(topic_id: str, name: str) -> Topic:
    """Rename a Topic.

    VR-003/004  name trimmed and non-empty
    VR-006      name unique case-insensitively (excluding self)
    REQ-F-059   auto-save after rename
    """
    # Confirm topic exists before validation
    if topic_repo.get_by_id(topic_id) is None:
        raise NotFoundError()

    trimmed = topic_validator.validate_rename(name, storage.get_topics(), topic_id)
    topic = topic_repo.rename(topic_id, trimmed)
    if topic is None:
        raise NotFoundError()

    storage.save()   # REQ-F-059
    log.info("topic.update  id=%s  name=%r", topic_id, trimmed)
    return topic


# ---------------------------------------------------------------------------
# REQ-F-026..029  Delete (with cascade unlink)
# ---------------------------------------------------------------------------


def delete_topic(topic_id: str) -> None:
    """Delete a Topic and cascade-unlink it from all MediaItems.

    REQ-F-028  Topic deleted from library
    REQ-F-029  MediaItems remain intact (only association removed)
    REQ-F-059  auto-save after deletion
    """
    if not topic_repo.delete(topic_id):
        raise NotFoundError()

    storage.save()   # REQ-F-059
    log.info("topic.delete  id=%s", topic_id)
