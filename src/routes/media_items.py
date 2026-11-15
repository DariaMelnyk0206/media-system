"""
src/routes/media_items.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP routes for MediaItem CRUD, status management, and Topic associations.

Base path: /api/media-items (registered in main.py with prefix="/api")

Endpoints:
  POST   /media-items                           createMediaItem        (FEAT-001)
  GET    /media-items                           listMediaItems         (FEAT-002)
  GET    /media-items/{id}                      getMediaItem           (FEAT-002)
  PATCH  /media-items/{id}                      updateMediaItem        (FEAT-002/003/005)
  DELETE /media-items/{id}                      deleteMediaItem        (FEAT-004)
  POST   /media-items/{id}/topics/{topicId}     addTopicToMediaItem    (FEAT-006)
  DELETE /media-items/{id}/topics/{topicId}     removeTopicFromMediaItem (FEAT-006)
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from src.errors.responses import err400, err404, err500
from src.logging.logger import get_logger
from src.models.media_item import (
    CreateMediaItemRequest,
    MediaItem,
    MediaItemListResponse,
    MediaStatus,
    MediaType,
    UpdateMediaItemRequest,
)
from src.services import association_service, media_item_service

log = get_logger(__name__)

router = APIRouter(prefix="/media-items", tags=["MediaItems"])
assoc_router = APIRouter(prefix="/media-items", tags=["MediaItemAssociations"])


# ---------------------------------------------------------------------------
# POST /media-items
# ---------------------------------------------------------------------------


@router.post(
    "",
    response_model=MediaItem,
    status_code=201,
    responses={400: err400, 404: err404, 500: err500},
)
def create_media_item(req: CreateMediaItemRequest) -> MediaItem:
    """Create a new MediaItem (FEAT-001, REQ-F-001..008).

    Validation (VR-001/002/007) and persistence (REQ-F-059) are delegated to
    the service layer.  Enum validation (VR-008/009) is handled by Pydantic.
    """
    return media_item_service.create_media_item(req)


# ---------------------------------------------------------------------------
# GET /media-items
# ---------------------------------------------------------------------------


@router.get(
    "",
    response_model=MediaItemListResponse,
    status_code=200,
    responses={400: err400},
)
def list_media_items(
    q: str | None = None,
    type: MediaType | None = None,
    status: MediaStatus | None = None,
    rating_min: int | None = None,
    rating_max: int | None = None,
    topic_id: str | None = None,
    sort: str | None = None,
    dir: str | None = "asc",
) -> MediaItemListResponse:
    """List MediaItems with optional search, filter, and sort (FEAT-002/008-011).

    Filtering, sorting, and rating-bound validation are handled by the service.
    """
    return media_item_service.list_media_items(
        q=q,
        media_type=type,
        status=status,
        rating_min=rating_min,
        rating_max=rating_max,
        topic_id=topic_id,
        sort=sort,
        direction=dir,
    )


# ---------------------------------------------------------------------------
# GET /media-items/{id}
# ---------------------------------------------------------------------------


@router.get(
    "/{item_id}",
    response_model=MediaItem,
    status_code=200,
    responses={404: err404},
)
def get_media_item(item_id: str) -> MediaItem:
    """Return a single MediaItem by id (FEAT-002, REQ-F-009)."""
    return media_item_service.get_media_item(item_id)


# ---------------------------------------------------------------------------
# PATCH /media-items/{id}
# ---------------------------------------------------------------------------


@router.patch(
    "/{item_id}",
    response_model=MediaItem,
    status_code=200,
    responses={400: err400, 404: err404, 500: err500},
)
def update_media_item(item_id: str, req: UpdateMediaItemRequest) -> MediaItem:
    """Partially update a MediaItem (FEAT-002/003/005, REQ-F-010..019)."""
    return media_item_service.update_media_item(item_id, req)


# ---------------------------------------------------------------------------
# DELETE /media-items/{id}
# ---------------------------------------------------------------------------


@router.delete(
    "/{item_id}",
    status_code=204,
    responses={404: err404, 500: err500},
)
def delete_media_item(item_id: str) -> Response:
    """Delete a MediaItem and all its Topic associations (FEAT-004, REQ-F-012..017)."""
    media_item_service.delete_media_item(item_id)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# POST /media-items/{id}/topics/{topicId}
# ---------------------------------------------------------------------------


@assoc_router.post(
    "/{item_id}/topics/{topic_id}",
    response_model=MediaItem,
    status_code=200,
    responses={404: err404, 500: err500},
)
def add_topic_to_media_item(item_id: str, topic_id: str) -> MediaItem:
    """Associate a Topic with a MediaItem (idempotent, REQ-F-030, DD-006)."""
    return association_service.add_topic_to_media_item(item_id, topic_id)


# ---------------------------------------------------------------------------
# DELETE /media-items/{id}/topics/{topicId}
# ---------------------------------------------------------------------------


@assoc_router.delete(
    "/{item_id}/topics/{topic_id}",
    status_code=204,
    responses={404: err404, 500: err500},
)
def remove_topic_from_media_item(item_id: str, topic_id: str) -> Response:
    """Remove a Topic association from a MediaItem (REQ-F-031)."""
    association_service.remove_topic_from_media_item(item_id, topic_id)
    return Response(status_code=204)
