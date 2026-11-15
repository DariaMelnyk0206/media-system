"""
src/services/media_item_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Business logic for MediaItem operations.

Covers FEAT-001..004 (Create, View, Edit, Delete, Status Management).
Each method:
  1. Validates input (via src/validators/media_item.py)
  2. Delegates to repository for data access
  3. Calls storage.save() after every mutation
  4. Raises domain exceptions (ValidationError, NotFoundError, SaveFailedError)
     so the route layer only needs to call the service and return the result.
"""

from __future__ import annotations

from src.errors.handlers import NotFoundError
from src.logging.logger import get_logger
from src.models.media_item import CreateMediaItemRequest, MediaItem, UpdateMediaItemRequest
from src.repository import media_item_repo, storage, topic_repo
from src.validators import media_item as validators

log = get_logger(__name__)


# ---------------------------------------------------------------------------
# FEAT-001  Create
# ---------------------------------------------------------------------------


def create_media_item(req: CreateMediaItemRequest) -> MediaItem:
    """Validate, create in-memory, save to disk.

    VR-001/002  name trimmed and non-empty
    VR-007      rating 1-10 or absent
    VR-008/009  enforced by Pydantic enum
    REQ-F-004   default status = planned (Pydantic default)
    REQ-F-007   topic_ids resolved to existing topics only
    REQ-F-059   auto-save after creation
    """
    trimmed = validators.validate_create(req.name, req.rating)
    # Resolve topic_ids: silently ignore unknown ids
    valid_topic_ids = [tid for tid in req.topic_ids if topic_repo.get_by_id(tid)]
    # Build a clean request with the trimmed name and validated topic_ids
    clean_req = req.model_copy(update={"name": trimmed, "topic_ids": valid_topic_ids})
    item = media_item_repo.create(clean_req)
    storage.save()   # REQ-F-059 — may raise SaveFailedError → 500
    log.info("service.create_media_item  id=%s", item.id)
    return item


# ---------------------------------------------------------------------------
# FEAT-002  View
# ---------------------------------------------------------------------------


def get_media_item(item_id: str) -> MediaItem:
    """Return a single MediaItem or raise NotFoundError."""
    item = media_item_repo.get_by_id(item_id)
    if item is None:
        log.debug("service.get_media_item  NOT_FOUND  id=%s", item_id)
        raise NotFoundError()
    return item


def list_media_items() -> list[MediaItem]:
    """Return all MediaItems (no filtering/sorting at this layer)."""
    return media_item_repo.list_all()


# ---------------------------------------------------------------------------
# FEAT-002 / FEAT-003  Edit (PATCH)
# ---------------------------------------------------------------------------


def update_media_item(item_id: str, req: UpdateMediaItemRequest) -> MediaItem:
    """Apply a partial update to a MediaItem.

    VR-001/002  name trimmed and non-empty (if name is being updated)
    VR-007      rating 1-10 or null (if rating is being updated)
    DD-004      absent fields are not changed
    DD-005      explicit null for notes/rating clears the field
    REQ-F-059   auto-save after edit
    """
    # Confirm item exists
    if media_item_repo.get_by_id(item_id) is None:
        raise NotFoundError()

    set_fields = req.model_fields_set

    # Validate and trim name if provided
    trimmed_name = validators.validate_update(req.name, req.rating, set_fields)

    # Apply trimmed name back to req if applicable
    effective_req = req
    if trimmed_name is not None:
        effective_req = req.model_copy(update={"name": trimmed_name})

    item = media_item_repo.update(item_id, effective_req, set_fields)
    if item is None:
        raise NotFoundError()

    storage.save()  # REQ-F-059
    log.info("service.update_media_item  id=%s  fields=%s", item_id, set_fields)
    return item


# ---------------------------------------------------------------------------
# FEAT-004  Delete
# ---------------------------------------------------------------------------


def delete_media_item(item_id: str) -> None:
    """Delete a MediaItem and its topic associations.

    REQ-F-012..016  deletion + association cleanup
    REQ-F-059       auto-save after deletion
    """
    if not media_item_repo.delete(item_id):
        raise NotFoundError()
    storage.save()  # REQ-F-059
    log.info("service.delete_media_item  id=%s", item_id)


# ---------------------------------------------------------------------------
# Association helpers (called from association routes, used in FEAT-006)
# ---------------------------------------------------------------------------


def add_topic_to_media_item(item_id: str, topic_id: str) -> MediaItem:
    """Associate a Topic with a MediaItem (idempotent, DD-006)."""
    if media_item_repo.get_by_id(item_id) is None:
        raise NotFoundError()
    if topic_repo.get_by_id(topic_id) is None:
        raise NotFoundError()
    item = media_item_repo.add_topic(item_id, topic_id)
    if item is None:
        raise NotFoundError()
    storage.save()
    return item


def remove_topic_from_media_item(item_id: str, topic_id: str) -> None:
    """Remove a Topic association from a MediaItem."""
    if media_item_repo.get_by_id(item_id) is None:
        raise NotFoundError()
    result = media_item_repo.remove_topic(item_id, topic_id)
    if result is None or result is False:
        raise NotFoundError()
    storage.save()
