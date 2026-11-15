"""
src/routes/media_items.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP routes for MediaItem CRUD, status management, and Topic associations.

Base path: /api/media-items (registered in main.py with prefix="/api")

Endpoints:
  POST   /media-items                           createMediaItem  (FEAT-001)
  GET    /media-items                           listMediaItems   (FEAT-002)
  GET    /media-items/{id}                      getMediaItem     (FEAT-002)
  PATCH  /media-items/{id}                      updateMediaItem  (FEAT-002/003/005)
  DELETE /media-items/{id}                      deleteMediaItem  (FEAT-004)
  POST   /media-items/{id}/topics/{topicId}     addTopicToMediaItem    (FEAT-006)
  DELETE /media-items/{id}/topics/{topicId}     removeTopicFromMediaItem (FEAT-006)
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from src.errors.error_codes import (
    INVALID_RATING_BOUND,
    INVALID_RATING_RANGE,
    INVALID_STATUS,
    INVALID_TYPE,
)
from src.errors.handlers import ValidationError
from src.logging.logger import get_logger
from src.models.media_item import (
    CreateMediaItemRequest,
    MediaItem,
    MediaStatus,
    MediaType,
    UpdateMediaItemRequest,
)
from src.services import association_service, media_item_service

log = get_logger(__name__)

router = APIRouter(prefix="/media-items", tags=["MediaItems"])


# ---------------------------------------------------------------------------
# POST /media-items
# ---------------------------------------------------------------------------


@router.post("", response_model=MediaItem, status_code=201)
def create_media_item(req: CreateMediaItemRequest) -> MediaItem:
    """Create a new MediaItem (FEAT-001, REQ-F-001..008).

    VR-001/002: name validated and trimmed by service layer.
    VR-007:     rating validated by service layer.
    VR-008/009: type/status validated by Pydantic enum.
    """
    return media_item_service.create_media_item(req)


# ---------------------------------------------------------------------------
# GET /media-items
# ---------------------------------------------------------------------------


@router.get("", response_model=dict, status_code=200)
def list_media_items(
    q: str | None = None,
    type: MediaType | None = None,
    status: MediaStatus | None = None,
    rating_min: int | None = None,
    rating_max: int | None = None,
    topic_id: str | None = None,
    sort: str | None = None,
    dir: str | None = "asc",
) -> dict:
    """List MediaItems with optional search, filter, and sort (FEAT-002/008/009/010/011).

    VR-010: rating_min must not exceed rating_max.
    VR-011: individual rating bounds must be 1-10.
    """
    # VR-011: validate individual bounds
    if rating_min is not None and not (1 <= rating_min <= 10):
        raise ValidationError(INVALID_RATING_BOUND, field="rating_min")
    if rating_max is not None and not (1 <= rating_max <= 10):
        raise ValidationError(INVALID_RATING_BOUND, field="rating_max")
    # VR-010: validate range
    if rating_min is not None and rating_max is not None and rating_min > rating_max:
        raise ValidationError(INVALID_RATING_RANGE, field="rating_min")

    items = media_item_service.list_media_items()

    # --- Search (REQ-F-038..042) ---
    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in i.name.lower()]

    # --- Filters ---
    if type is not None:
        items = [i for i in items if i.type == type]
    if status is not None:
        items = [i for i in items if i.status == status]
    if topic_id is not None:
        items = [i for i in items if any(t.id == topic_id for t in i.topics)]

    # Rating filter — unrated items always excluded when any bound active (REQ-F-048)
    if rating_min is not None or rating_max is not None:
        items = [i for i in items if i.rating is not None]
        if rating_min is not None:
            items = [i for i in items if i.rating >= rating_min]
        if rating_max is not None:
            items = [i for i in items if i.rating <= rating_max]

    # --- Sort (REQ-F-051..055) ---
    if sort == "name":
        reverse = dir == "desc"
        items = sorted(items, key=lambda i: i.name.lower(), reverse=reverse)
    elif sort == "rating":
        reverse = dir == "desc"
        # Unrated always last (REQ-F-055)
        rated = [i for i in items if i.rating is not None]
        unrated = [i for i in items if i.rating is None]
        rated_sorted = sorted(rated, key=lambda i: i.rating, reverse=reverse)
        items = rated_sorted + unrated

    return {"data": items, "total": len(items)}


# ---------------------------------------------------------------------------
# GET /media-items/{id}
# ---------------------------------------------------------------------------


@router.get("/{item_id}", response_model=MediaItem, status_code=200)
def get_media_item(item_id: str) -> MediaItem:
    """Return a single MediaItem (FEAT-002, REQ-F-009)."""
    return media_item_service.get_media_item(item_id)


# ---------------------------------------------------------------------------
# PATCH /media-items/{id}
# ---------------------------------------------------------------------------


@router.patch("/{item_id}", response_model=MediaItem, status_code=200)
def update_media_item(item_id: str, req: UpdateMediaItemRequest) -> MediaItem:
    """Partially update a MediaItem (FEAT-002/003/005, REQ-F-010..019)."""
    return media_item_service.update_media_item(item_id, req)


# ---------------------------------------------------------------------------
# DELETE /media-items/{id}
# ---------------------------------------------------------------------------


@router.delete("/{item_id}", status_code=204)
def delete_media_item(item_id: str) -> Response:
    """Delete a MediaItem and its associations (FEAT-004, REQ-F-012..017)."""
    media_item_service.delete_media_item(item_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /media-items/{id}/topics/{topicId}
# ---------------------------------------------------------------------------

assoc_router = APIRouter(prefix="/media-items", tags=["MediaItemAssociations"])


@assoc_router.post("/{item_id}/topics/{topic_id}", response_model=MediaItem, status_code=200)
def add_topic_to_media_item(item_id: str, topic_id: str) -> MediaItem:
    """Associate a Topic with a MediaItem (idempotent, DD-006, REQ-F-030).

    404 if either entity does not exist.
    Logs: association.link
    """
    return association_service.add_topic_to_media_item(item_id, topic_id)


@assoc_router.delete("/{item_id}/topics/{topic_id}", status_code=204)
def remove_topic_from_media_item(item_id: str, topic_id: str) -> Response:
    """Remove Topic association from a MediaItem (REQ-F-031).

    404 if the association does not exist.
    Logs: association.unlink
    """
    association_service.remove_topic_from_media_item(item_id, topic_id)
    return Response(status_code=204)
