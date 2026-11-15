"""
tests/unit/test_media_item_create.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-001 — MediaItem Create (позитивні сценарії)
TEST-002 — MediaItem Create (негативні / валідація)

SRS coverage:
  AC-001  name + type → MediaItem created
  AC-002  default status = planned
  AC-003  notes empty / rating unset allowed
  AC-004  topic_ids assigned on creation
  AC-042  empty / whitespace-only name rejected (VR-001)
  AC-043  name trimmed (VR-002)
  AC-044  rating outside 1-10 rejected (VR-007)
  AC-064  type must be one of 7 valid values (VR-008)
  AC-065  status must be one of 5 valid values (VR-009)
  AC-060  default status field pre-selected as planned

BDD coverage: BDD-001, BDD-002, BDD-004, BDD-005, BDD-006, BDD-007, BDD-008
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import (
    ERR_INVALID_STATUS,
    ERR_INVALID_TYPE,
    ERR_NAME_REQUIRED,
    ERR_RATING_OUT_OF_RANGE,
    FIELD_NAME,
    FIELD_RATING,
    FIELD_STATUS,
    FIELD_TYPE,
    MEDIA_EMPTY_NAME,
    MEDIA_FULL,
    MEDIA_INVALID_STATUS,
    MEDIA_INVALID_TYPE,
    MEDIA_MINIMAL,
    MEDIA_PADDED_NAME,
    MEDIA_PADDED_NAME_EXPECTED,
    MEDIA_RATING_NEGATIVE,
    MEDIA_RATING_TOO_HIGH,
    MEDIA_RATING_ZERO,
    MEDIA_WHITESPACE_NAME,
)

BASE = "/api/media-items"

# ---------------------------------------------------------------------------
# TEST-001  Позитивні сценарії (AC-001..004, AC-060)
# ---------------------------------------------------------------------------


class TestMediaItemCreatePositive:
    """TEST-001: positive create scenarios."""

    def test_create_minimal_returns_201(self, client: TestClient) -> None:
        """BDD-001 / AC-001: required fields only → 201 with MediaItem body."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        assert resp.status_code == 201, resp.text

    def test_create_minimal_response_shape(self, client: TestClient) -> None:
        """AC-001: response contains all required MediaItem fields."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        body = resp.json()
        for field in ("id", "name", "type", "status", "notes", "rating", "topics"):
            assert field in body, f"Missing field: {field}"

    def test_create_minimal_name_and_type(self, client: TestClient) -> None:
        """AC-001: name and type are stored as submitted."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        body = resp.json()
        assert body["name"] == MEDIA_MINIMAL["name"]
        assert body["type"] == MEDIA_MINIMAL["type"]

    def test_create_default_status_is_planned(self, client: TestClient) -> None:
        """BDD-001 / AC-002 / AC-060: status defaults to 'planned'."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        assert resp.json()["status"] == "planned"

    def test_create_default_notes_null(self, client: TestClient) -> None:
        """AC-003: notes is null when not supplied."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        assert resp.json()["notes"] is None

    def test_create_default_rating_null(self, client: TestClient) -> None:
        """AC-003: rating is null when not supplied."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        assert resp.json()["rating"] is None

    def test_create_default_topics_empty(self, client: TestClient) -> None:
        """AC-003: topics list is empty when not supplied."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        assert resp.json()["topics"] == []

    def test_create_id_is_string(self, client: TestClient) -> None:
        """AC-001: id field is a non-empty string (UUID)."""
        resp = client.post(BASE, json=MEDIA_MINIMAL)
        item_id = resp.json()["id"]
        assert isinstance(item_id, str) and len(item_id) > 0

    def test_create_full_payload(self, client: TestClient) -> None:
        """BDD-002 / AC-001, AC-003: all optional fields stored correctly."""
        resp = client.post(BASE, json=MEDIA_FULL)
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == MEDIA_FULL["name"]
        assert body["type"] == MEDIA_FULL["type"]
        assert body["status"] == MEDIA_FULL["status"]
        assert body["notes"] == MEDIA_FULL["notes"]
        assert body["rating"] == MEDIA_FULL["rating"]

    def test_create_explicit_status(self, client: TestClient) -> None:
        """AC-012: any valid status can be set at creation."""
        payload = {"name": "Test Item", "type": "movie", "status": "in_progress"}
        resp = client.post(BASE, json=payload)
        assert resp.status_code == 201
        assert resp.json()["status"] == "in_progress"

    def test_create_name_is_trimmed(self, client: TestClient) -> None:
        """BDD-006 / AC-043 / VR-002: leading/trailing whitespace removed."""
        resp = client.post(BASE, json=MEDIA_PADDED_NAME)
        assert resp.status_code == 201
        assert resp.json()["name"] == MEDIA_PADDED_NAME_EXPECTED

    def test_create_with_topic_ids(self, client: TestClient) -> None:
        """AC-004: topic_ids provided at creation → topics list reflects them."""
        # Create a topic first so we have a valid topic_id
        t_resp = client.post("/api/topics", json={"name": "Science Fiction"})
        assert t_resp.status_code == 201
        topic_id = t_resp.json()["id"]

        payload = {**MEDIA_MINIMAL, "topic_ids": [topic_id]}
        resp = client.post(BASE, json=payload)
        assert resp.status_code == 201
        topics = resp.json()["topics"]
        assert any(t["id"] == topic_id for t in topics)

    @pytest.mark.parametrize(
        "media_type",
        ["book", "movie", "tv_series", "article", "podcast", "video", "other"],
    )
    def test_create_all_valid_types(
        self, client: TestClient, media_type: str
    ) -> None:
        """AC-064 / VR-008: all 7 MediaType enum values are accepted."""
        payload = {"name": f"Item {media_type}", "type": media_type}
        resp = client.post(BASE, json=payload)
        assert resp.status_code == 201
        assert resp.json()["type"] == media_type

    @pytest.mark.parametrize(
        "status",
        ["planned", "in_progress", "postponed", "abandoned", "completed"],
    )
    def test_create_all_valid_statuses(
        self, client: TestClient, status: str
    ) -> None:
        """AC-065 / VR-009: all 5 MediaStatus enum values are accepted."""
        payload = {"name": f"Item {status}", "type": "book", "status": status}
        resp = client.post(BASE, json=payload)
        assert resp.status_code == 201
        assert resp.json()["status"] == status

    @pytest.mark.parametrize("rating", [1, 5, 10])
    def test_create_valid_ratings(self, client: TestClient, rating: int) -> None:
        """VR-007 boundary: ratings 1, 5, 10 are accepted."""
        payload = {"name": f"Rated {rating}", "type": "book", "rating": rating}
        resp = client.post(BASE, json=payload)
        assert resp.status_code == 201
        assert resp.json()["rating"] == rating


# ---------------------------------------------------------------------------
# TEST-002  Негативні / валідація (AC-042, AC-044, AC-064, AC-065)
# ---------------------------------------------------------------------------


class TestMediaItemCreateValidation:
    """TEST-002: negative and validation scenarios."""

    # --- VR-001: empty name ---

    def test_empty_name_rejected_400(self, client: TestClient) -> None:
        """BDD-004 / AC-042 / VR-001: empty name → 400."""
        resp = client.post(BASE, json=MEDIA_EMPTY_NAME)
        assert resp.status_code == 400, resp.text

    def test_empty_name_error_code(self, client: TestClient) -> None:
        """BDD-004 / AC-042: error.error == 'name_required'."""
        resp = client.post(BASE, json=MEDIA_EMPTY_NAME)
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    def test_empty_name_error_field(self, client: TestClient) -> None:
        """BDD-004 / AC-042: error.field == 'name'."""
        resp = client.post(BASE, json=MEDIA_EMPTY_NAME)
        assert resp.json()["field"] == FIELD_NAME

    def test_empty_name_error_message_present(self, client: TestClient) -> None:
        """AC-042: error.message is a non-empty string."""
        resp = client.post(BASE, json=MEDIA_EMPTY_NAME)
        assert isinstance(resp.json()["message"], str)
        assert len(resp.json()["message"]) > 0

    # --- VR-001: whitespace-only name ---

    def test_whitespace_name_rejected_400(self, client: TestClient) -> None:
        """BDD-005 / AC-042 / VR-001: whitespace-only name → 400."""
        resp = client.post(BASE, json=MEDIA_WHITESPACE_NAME)
        assert resp.status_code == 400, resp.text

    def test_whitespace_name_error_code(self, client: TestClient) -> None:
        """BDD-005 / AC-042: error.error == 'name_required'."""
        resp = client.post(BASE, json=MEDIA_WHITESPACE_NAME)
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    def test_whitespace_name_error_field(self, client: TestClient) -> None:
        """BDD-005 / AC-042: error.field == 'name'."""
        resp = client.post(BASE, json=MEDIA_WHITESPACE_NAME)
        assert resp.json()["field"] == FIELD_NAME

    # --- VR-007: rating out of range ---

    def test_rating_too_high_rejected(self, client: TestClient) -> None:
        """BDD-007 / AC-044 / VR-007: rating 11 → 400."""
        resp = client.post(BASE, json=MEDIA_RATING_TOO_HIGH)
        assert resp.status_code == 400, resp.text

    def test_rating_too_high_error_code(self, client: TestClient) -> None:
        """BDD-007 / AC-044: error.error == 'rating_out_of_range'."""
        resp = client.post(BASE, json=MEDIA_RATING_TOO_HIGH)
        assert resp.json()["error"] == ERR_RATING_OUT_OF_RANGE

    def test_rating_too_high_error_field(self, client: TestClient) -> None:
        """BDD-007 / AC-044: error.field == 'rating'."""
        resp = client.post(BASE, json=MEDIA_RATING_TOO_HIGH)
        assert resp.json()["field"] == FIELD_RATING

    def test_rating_zero_rejected(self, client: TestClient) -> None:
        """BDD-008 / AC-044 / VR-007: rating 0 → 400."""
        resp = client.post(BASE, json=MEDIA_RATING_ZERO)
        assert resp.status_code == 400, resp.text

    def test_rating_zero_error_code(self, client: TestClient) -> None:
        """BDD-008 / AC-044: error.error == 'rating_out_of_range'."""
        resp = client.post(BASE, json=MEDIA_RATING_ZERO)
        assert resp.json()["error"] == ERR_RATING_OUT_OF_RANGE

    def test_rating_negative_rejected(self, client: TestClient) -> None:
        """VR-007 boundary: negative rating → 400."""
        resp = client.post(BASE, json=MEDIA_RATING_NEGATIVE)
        assert resp.status_code == 400, resp.text

    # --- VR-008: invalid type ---

    def test_invalid_type_rejected(self, client: TestClient) -> None:
        """VR-008 / AC-064: unknown type value → 400."""
        resp = client.post(BASE, json=MEDIA_INVALID_TYPE)
        assert resp.status_code == 400, resp.text

    def test_invalid_type_error_code(self, client: TestClient) -> None:
        """VR-008: error.error == 'invalid_type'."""
        resp = client.post(BASE, json=MEDIA_INVALID_TYPE)
        assert resp.json()["error"] == ERR_INVALID_TYPE

    def test_invalid_type_error_field(self, client: TestClient) -> None:
        """VR-008: error.field == 'type'."""
        resp = client.post(BASE, json=MEDIA_INVALID_TYPE)
        assert resp.json()["field"] == FIELD_TYPE

    # --- VR-009: invalid status ---

    def test_invalid_status_rejected(self, client: TestClient) -> None:
        """VR-009 / AC-065: unknown status value → 400."""
        resp = client.post(BASE, json=MEDIA_INVALID_STATUS)
        assert resp.status_code == 400, resp.text

    def test_invalid_status_error_code(self, client: TestClient) -> None:
        """VR-009: error.error == 'invalid_status'."""
        resp = client.post(BASE, json=MEDIA_INVALID_STATUS)
        assert resp.json()["error"] == ERR_INVALID_STATUS

    def test_invalid_status_error_field(self, client: TestClient) -> None:
        """VR-009: error.field == 'status'."""
        resp = client.post(BASE, json=MEDIA_INVALID_STATUS)
        assert resp.json()["field"] == FIELD_STATUS

    # --- Missing required fields ---

    def test_missing_name_rejected(self, client: TestClient) -> None:
        """VR-001: name field absent entirely → 400 (or 422)."""
        resp = client.post(BASE, json={"type": "book"})
        assert resp.status_code in (400, 422), resp.text

    def test_missing_type_rejected(self, client: TestClient) -> None:
        """VR-008: type field absent entirely → 400 (or 422)."""
        resp = client.post(BASE, json={"name": "No Type"})
        assert resp.status_code in (400, 422), resp.text

    # --- ErrorResponse shape invariant ---

    def test_error_response_has_all_fields(self, client: TestClient) -> None:
        """api-design-spec §3: ErrorResponse always has error, field, message."""
        resp = client.post(BASE, json=MEDIA_EMPTY_NAME)
        body = resp.json()
        for key in ("error", "field", "message"):
            assert key in body, f"ErrorResponse missing key: {key}"
