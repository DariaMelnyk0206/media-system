"""
src/routes/topics.py
~~~~~~~~~~~~~~~~~~~~~
HTTP routes for Topic CRUD and Topic–MediaItem associations.

Endpoints:
  POST   /topics                              createTopic         (FEAT-005)
  GET    /topics                              listTopics          (FEAT-005)
  GET    /topics/{id}                         getTopic            (FEAT-005)
  PATCH  /topics/{id}                         updateTopic         (FEAT-005)
  DELETE /topics/{id}                         deleteTopic         (FEAT-005)
  POST   /topics/{id}/media-items/{mediaId}   addMediaItemToTopic (FEAT-006)
  DELETE /topics/{id}/media-items/{mediaId}   removeMediaItemFromTopic (FEAT-006)
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from src.errors import error_codes
from src.errors.handlers import ConflictError, NotFoundError, ValidationError
from src.logging.logger import get_logger
from src.models.topic import CreateTopicRequest, Topic, TopicSummary, UpdateTopicRequest
from src.repository import storage, topic_repo
from src.repository import media_item_repo
from src.models.media_item import MediaItem

log = get_logger(__name__)

router = APIRouter(prefix="/topics", tags=["Topics"])
assoc_router = APIRouter(prefix="/topics", tags=["TopicAssociations"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validate_topic_name(name: str) -> str:
    """Trim and validate a Topic name (VR-003, VR-004)."""
    trimmed = name.strip()
    if not trimmed:
        raise ValidationError(error_codes.NAME_REQUIRED, field="name")
    return trimmed


def _check_unique(name_lower: str, exclude_id: str | None = None) -> None:
    """Raise ConflictError if name already in use (VR-005, VR-006)."""
    existing = topic_repo.find_by_name_ci(name_lower)
    if existing and existing["id"] != exclude_id:
        raise ConflictError(error_codes.NAME_TAKEN, field="name")


# ---------------------------------------------------------------------------
# POST /topics
# ---------------------------------------------------------------------------


@router.post("", response_model=Topic, status_code=201)
def create_topic(req: CreateTopicRequest) -> Topic:
    """Create a new Topic (FEAT-005, REQ-F-020..021)."""
    trimmed = _validate_topic_name(req.name)
    _check_unique(trimmed)
    topic = topic_repo.create(trimmed)
    storage.save()
    log.info("route.create_topic  id=%s  name=%r", topic.id, trimmed)
    return topic


# ---------------------------------------------------------------------------
# GET /topics
# ---------------------------------------------------------------------------


@router.get("", response_model=dict, status_code=200)
def list_topics() -> dict:
    """List all Topics (FEAT-005, REQ-F-022)."""
    return {"data": topic_repo.list_all()}


# ---------------------------------------------------------------------------
# GET /topics/{id}
# ---------------------------------------------------------------------------


@router.get("/{topic_id}", response_model=Topic, status_code=200)
def get_topic(topic_id: str) -> Topic:
    """Get a single Topic (FEAT-005, REQ-F-022)."""
    topic = topic_repo.get_by_id(topic_id)
    if topic is None:
        raise NotFoundError()
    return topic


# ---------------------------------------------------------------------------
# PATCH /topics/{id}
# ---------------------------------------------------------------------------


@router.patch("/{topic_id}", response_model=Topic, status_code=200)
def update_topic(topic_id: str, req: UpdateTopicRequest) -> Topic:
    """Rename a Topic (FEAT-005, REQ-F-023..025)."""
    existing = topic_repo.get_by_id(topic_id)
    if existing is None:
        raise NotFoundError()
    trimmed = _validate_topic_name(req.name)
    # VR-006: check uniqueness, excluding the current topic itself
    _check_unique(trimmed, exclude_id=topic_id)
    topic = topic_repo.rename(topic_id, trimmed)
    if topic is None:
        raise NotFoundError()
    storage.save()
    log.info("route.update_topic  id=%s  name=%r", topic_id, trimmed)
    return topic


# ---------------------------------------------------------------------------
# DELETE /topics/{id}
# ---------------------------------------------------------------------------


@router.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: str) -> Response:
    """Delete a Topic (FEAT-005, REQ-F-026..029)."""
    if not topic_repo.delete(topic_id):
        raise NotFoundError()
    storage.save()
    log.info("route.delete_topic  id=%s", topic_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /topics/{id}/media-items/{mediaId}
# ---------------------------------------------------------------------------


@assoc_router.post("/{topic_id}/media-items/{media_id}", response_model=Topic, status_code=200)
def add_media_item_to_topic(topic_id: str, media_id: str) -> Topic:
    """Associate a MediaItem with a Topic (FEAT-006, REQ-F-032)."""
    topic = topic_repo.add_media_item(topic_id, media_id)
    if topic is None:
        raise NotFoundError()
    storage.save()
    return topic


# ---------------------------------------------------------------------------
# DELETE /topics/{id}/media-items/{mediaId}
# ---------------------------------------------------------------------------


@assoc_router.delete("/{topic_id}/media-items/{media_id}", status_code=204)
def remove_media_item_from_topic(topic_id: str, media_id: str) -> Response:
    """Remove a MediaItem association from a Topic (FEAT-006, REQ-F-033)."""
    result = topic_repo.remove_media_item(topic_id, media_id)
    if result is None or result is False:
        raise NotFoundError()
    storage.save()
    return Response(status_code=204)
