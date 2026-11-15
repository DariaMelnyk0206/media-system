"""
src/services/media_item_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business logic for MediaItem CRUD and status management.

Covers FEAT-001..004 (Create, View, Edit, Delete).

Each method:
  1. Validates input (via src/validators/media_item.py).
  2. Delegates to repository for data access.
  3. Calls storage.save() after every mutation (REQ-F-059).
  4. Raises domain exceptions (ValidationError, NotFoundError, SaveFailedError)
     so the route layer only needs to call the service and return the result.

MediaItem–Topic association operations live in association_service.py (FEAT-006,
REQ-F-030..034), keeping this module focused on the MediaItem lifecycle only.
"""

from __future__ import annotations

from src.errors.handlers import NotFoundError
from src.logging.logger import get_logger
from src.models.media_item import (
    CreateMediaItemRequest,
    MediaItem,
    MediaItemListResponse,
    MediaStatus,
    MediaType,
    UpdateMediaItemRequest,
)
from src.repository import media_item_repo, storage, topic_repo
from src.validators import media_item as validators

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# FEAT-001  Create
# ---------------------------------------------------------------------------


def create_media_item(req: CreateMediaItemRequest) -> MediaItem:
    """Validate, create in-memory, and persist to disk.

    VR-001/002  name trimmed and non-empty.
    VR-007      rating 1-10 or absent.
    VR-008/009  enforced by Pydantic enum parsing upstream.
    REQ-F-004   default status = planned (Pydantic default on the request model).
    REQ-F-007   topic_ids silently filtered to existing topics only.
    REQ-F-059   auto-save after creation; may raise SaveFailedError (500).
    """
    trimmed = validators.validate_create(req.name, req.rating)
    valid_topic_ids = [tid for tid in req.topic_ids if topic_repo.get_by_id(tid) is not None]
    clean_req = req.model_copy(update={"name": trimmed, "topic_ids": valid_topic_ids})
    item = media_item_repo.create(clean_req)
    storage.save()
    log.info("service.create_media_item  id=%s", item.id)
    return item


# ---------------------------------------------------------------------------
# FEAT-002  View
# ---------------------------------------------------------------------------


def get_media_item(item_id: str) -> MediaItem:
    """Return a single MediaItem or raise NotFoundError (404)."""
    item = media_item_repo.get_by_id(item_id)
    if item is None:
        log.debug("service.get_media_item  NOT_FOUND  id=%s", item_id)
        raise NotFoundError()
    return item


def list_media_items(
    q: str | None = None,
    media_type: MediaType | None = None,
    status: MediaStatus | None = None,
    rating_min: int | None = None,
    rating_max: int | None = None,
    topic_id: str | None = None,
    sort: str | None = None,
    direction: str | None = "asc",
) -> MediaItemListResponse:
    """Filter and sort MediaItems for the collection endpoint."""
    validators.validate_rating_bounds(rating_min, rating_max)

    items = media_item_repo.list_all()
    if q:
        query = q.lower()
        items = [item for item in items if query in item.name.lower()]
    if media_type is not None:
        items = [item for item in items if item.type == media_type]
    if status is not None:
        items = [item for item in items if item.status == status]
    if topic_id is not None:
        items = [item for item in items if any(topic.id == topic_id for topic in item.topics)]

    if rating_min is not None or rating_max is not None:
        items = [item for item in items if item.rating is not None]
        if rating_min is not None:
            items = [item for item in items if item.rating is not None and item.rating >= rating_min]
        if rating_max is not None:
            items = [item for item in items if item.rating is not None and item.rating <= rating_max]

    reverse = direction == "desc"
    if sort == "name":
        items = sorted(items, key=lambda item: item.name.lower(), reverse=reverse)
    elif sort == "rating":
        rated = [item for item in items if item.rating is not None]
        rated.sort(
            key=lambda item: item.rating if item.rating is not None else 0,
            reverse=reverse,
        )
        unrated = [item for item in items if item.rating is None]
        items = rated + unrated

    return MediaItemListResponse(data=items, total=len(items))


# ---------------------------------------------------------------------------
# FEAT-002 / FEAT-003  Edit (PATCH)
# ---------------------------------------------------------------------------


def update_media_item(item_id: str, req: UpdateMediaItemRequest) -> MediaItem:
    """Apply a partial update to an existing MediaItem.

    DD-004  Absent fields are not changed.
    DD-005  Explicit null for notes/rating clears the field.
    VR-001/002  name trimmed and non-empty when provided.
    VR-007      rating 1-10 or null when provided.
    REQ-F-059   auto-save after edit; may raise SaveFailedError (500).
    """
    if media_item_repo.get_by_id(item_id) is None:
        raise NotFoundError()

    set_fields = req.model_fields_set
    trimmed_name = validators.validate_update(req.name, req.rating, set_fields)

    effective_req = req
    if trimmed_name is not None:
        effective_req = req.model_copy(update={"name": trimmed_name})

    item = media_item_repo.update(item_id, effective_req, set_fields)
    if item is None:
        raise NotFoundError()

    storage.save()
    log.info("service.update_media_item  id=%s  fields=%s", item_id, set_fields)
    return item


# ---------------------------------------------------------------------------
# FEAT-004  Delete
# ---------------------------------------------------------------------------


def delete_media_item(item_id: str) -> None:
    """Delete a MediaItem and remove all its Topic associations.

    REQ-F-012..016  deletion and association cleanup.
    REQ-F-059       auto-save after deletion; may raise SaveFailedError (500).
    """
    if not media_item_repo.delete(item_id):
        raise NotFoundError()
    storage.save()
    log.info("service.delete_media_item  id=%s", item_id)
