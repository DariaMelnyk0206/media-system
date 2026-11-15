"""
src/routes/topics.py
~~~~~~~~~~~~~~~~~~~~~
HTTP routes for Topic CRUD and Topic–MediaItem associations.

Endpoints:
  POST   /topics                              createTopic         (FEAT-005, REQ-F-020..021)
  GET    /topics                              listTopics          (FEAT-005, REQ-F-022)
  GET    /topics/{id}                         getTopic            (FEAT-005, REQ-F-022)
  PATCH  /topics/{id}                         updateTopic         (FEAT-005, REQ-F-023..025)
  DELETE /topics/{id}                         deleteTopic         (FEAT-005, REQ-F-026..029)
  POST   /topics/{id}/media-items/{mediaId}   addMediaItemToTopic (FEAT-006, REQ-F-032)
  DELETE /topics/{id}/media-items/{mediaId}   removeMediaItemFromTopic (FEAT-006, REQ-F-033)

All validation, persistence, and logging are delegated to the service layer.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from src.logging.logger import get_logger
from src.models.topic import CreateTopicRequest, Topic, TopicSummary, UpdateTopicRequest
from src.services import association_service, topic_service

log = get_logger(__name__)

router = APIRouter(prefix="/topics", tags=["Topics"])
assoc_router = APIRouter(prefix="/topics", tags=["TopicAssociations"])


# ---------------------------------------------------------------------------
# POST /topics
# ---------------------------------------------------------------------------


@router.post("", response_model=Topic, status_code=201)
def create_topic(req: CreateTopicRequest) -> Topic:
    """Create a new Topic (FEAT-005, REQ-F-020..021).

    VR-003/004: name trimmed and non-empty (service layer).
    VR-005:     name unique case-insensitively (service layer).
    REQ-F-059:  auto-save (service layer).
    Logs: topic.create
    """
    return topic_service.create_topic(req.name)


# ---------------------------------------------------------------------------
# GET /topics
# ---------------------------------------------------------------------------


@router.get("", response_model=dict, status_code=200)
def list_topics() -> dict:
    """List all Topics as TopicSummary objects (FEAT-005, REQ-F-022)."""
    return {"data": topic_service.list_topics()}


# ---------------------------------------------------------------------------
# GET /topics/{id}
# ---------------------------------------------------------------------------


@router.get("/{topic_id}", response_model=Topic, status_code=200)
def get_topic(topic_id: str) -> Topic:
    """Return a single Topic with its media_items (FEAT-005, REQ-F-022)."""
    return topic_service.get_topic(topic_id)


# ---------------------------------------------------------------------------
# PATCH /topics/{id}
# ---------------------------------------------------------------------------


@router.patch("/{topic_id}", response_model=Topic, status_code=200)
def update_topic(topic_id: str, req: UpdateTopicRequest) -> Topic:
    """Rename a Topic (FEAT-005, REQ-F-023..025).

    VR-003/004: name trimmed and non-empty (service layer).
    VR-006:     uniqueness check excluding self (service layer).
    REQ-F-059:  auto-save (service layer).
    Logs: topic.update
    """
    return topic_service.update_topic(topic_id, req.name)


# ---------------------------------------------------------------------------
# DELETE /topics/{id}
# ---------------------------------------------------------------------------


@router.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: str) -> Response:
    """Delete a Topic and unlink it from all MediaItems (FEAT-005, REQ-F-026..029).

    REQ-F-029: MediaItems remain intact.
    REQ-F-059: auto-save (service layer).
    Logs: topic.delete
    """
    topic_service.delete_topic(topic_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /topics/{id}/media-items/{mediaId}
# ---------------------------------------------------------------------------


@assoc_router.post("/{topic_id}/media-items/{media_id}", response_model=Topic, status_code=200)
def add_media_item_to_topic(topic_id: str, media_id: str) -> Topic:
    """Associate a MediaItem with a Topic (idempotent, FEAT-006, REQ-F-032).

    404 if either entity does not exist.
    Logs: association.link
    """
    return association_service.add_media_item_to_topic(topic_id, media_id)


# ---------------------------------------------------------------------------
# DELETE /topics/{id}/media-items/{mediaId}
# ---------------------------------------------------------------------------


@assoc_router.delete("/{topic_id}/media-items/{media_id}", status_code=204)
def remove_media_item_from_topic(topic_id: str, media_id: str) -> Response:
    """Remove a MediaItem association from a Topic (FEAT-006, REQ-F-033).

    404 if the association does not exist.
    Logs: association.unlink
    """
    association_service.remove_media_item_from_topic(topic_id, media_id)
    return Response(status_code=204)
