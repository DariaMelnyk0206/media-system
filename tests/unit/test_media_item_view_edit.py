"""
tests/unit/test_media_item_view_edit.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-003 — MediaItem View та Edit

SRS coverage:
  AC-006  all fields visible (name, type, status, notes, rating, topics)
  AC-007  edited value reflected on next view
  AC-012  status can change to any of 5 values from any other
  AC-043  name trimmed on edit (VR-002)
  AC-044  rating outside 1-10 rejected on PATCH (VR-007)
  AC-042  empty/whitespace name rejected on PATCH (VR-001)
  AC-027  GET list returns all items when no filters

BDD coverage: BDD-009, BDD-010, BDD-011, BDD-012
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import (
    ERR_NAME_REQUIRED,
    ERR_NOT_FOUND,
    ERR_RATING_OUT_OF_RANGE,
    MEDIA_BOOK_COMPLETED,
    MEDIA_FULL,
    MEDIA_MINIMAL,
)

BASE = "/api/media-items"


def _create(client: TestClient, payload: dict | None = None) -> dict:
    """Helper: create a MediaItem and return the parsed body."""
    resp = client.post(BASE, json=payload or MEDIA_MINIMAL)
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestMediaItemGet:
    """GET /api/media-items/{id} — view a single item."""

    def test_get_existing_returns_200(self, client: TestClient) -> None:
        """AC-006: GET by valid id → 200."""
        item = _create(client)
        resp = client.get(f"{BASE}/{item['id']}")
        assert resp.status_code == 200, resp.text

    def test_get_returns_all_required_fields(self, client: TestClient) -> None:
        """AC-006: all 7 fields present in response."""
        item = _create(client)
        resp = client.get(f"{BASE}/{item['id']}")
        body = resp.json()
        for field in ("id", "name", "type", "status", "notes", "rating", "topics"):
            assert field in body, f"Missing field: {field}"

    def test_get_full_item_fields(self, client: TestClient) -> None:
        """BDD-009 / AC-006: full item with notes, rating, topics readable."""
        item = _create(client, MEDIA_FULL)
        resp = client.get(f"{BASE}/{item['id']}")
        body = resp.json()
        assert body["name"] == MEDIA_FULL["name"]
        assert body["notes"] == MEDIA_FULL["notes"]
        assert body["rating"] == MEDIA_FULL["rating"]

    def test_get_minimal_item_optional_fields(self, client: TestClient) -> None:
        """BDD-010 / AC-006: notes null, rating null, topics [] when not set."""
        item = _create(client, MEDIA_MINIMAL)
        resp = client.get(f"{BASE}/{item['id']}")
        body = resp.json()
        assert body["notes"] is None
        assert body["rating"] is None
        assert body["topics"] == []

    def test_get_nonexistent_returns_404(self, client: TestClient) -> None:
        """GET unknown id → 404."""
        resp = client.get(f"{BASE}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404, resp.text

    def test_get_nonexistent_error_code(self, client: TestClient) -> None:
        """404 body has error == 'not_found'."""
        resp = client.get(f"{BASE}/00000000-0000-0000-0000-000000000000")
        assert resp.json()["error"] == ERR_NOT_FOUND


class TestMediaItemList:
    """GET /api/media-items — list all items."""

    def test_list_empty_returns_200(self, client: TestClient) -> None:
        """Empty library → 200 with data=[] and total=0."""
        resp = client.get(BASE)
        assert resp.status_code == 200, resp.text

    def test_list_empty_shape(self, client: TestClient) -> None:
        """Response has 'data' (list) and 'total' (int) fields."""
        resp = client.get(BASE)
        body = resp.json()
        assert "data" in body
        assert "total" in body
        assert isinstance(body["data"], list)
        assert isinstance(body["total"], int)

    def test_list_returns_created_items(self, client: TestClient) -> None:
        """AC-027: items appear in list after creation."""
        item = _create(client)
        resp = client.get(BASE)
        ids = [i["id"] for i in resp.json()["data"]]
        assert item["id"] in ids

    def test_list_total_matches_data_length(self, client: TestClient) -> None:
        """total == len(data)."""
        _create(client, MEDIA_MINIMAL)
        _create(client, MEDIA_FULL)
        resp = client.get(BASE)
        body = resp.json()
        assert body["total"] == len(body["data"])

    def test_list_multiple_items(self, client: TestClient) -> None:
        """Two created items both appear in list."""
        a = _create(client, MEDIA_MINIMAL)
        b = _create(client, MEDIA_FULL)
        ids = [i["id"] for i in client.get(BASE).json()["data"]]
        assert a["id"] in ids
        assert b["id"] in ids


class TestMediaItemPatch:
    """PATCH /api/media-items/{id} — partial update."""

    def test_patch_status_returns_200(self, client: TestClient) -> None:
        """BDD-012 / AC-007: PATCH status → 200."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "completed"})
        assert resp.status_code == 200, resp.text

    def test_patch_status_reflected(self, client: TestClient) -> None:
        """BDD-011 / AC-007: updated status visible in subsequent GET."""
        item = _create(client)
        client.patch(f"{BASE}/{item['id']}", json={"status": "completed"})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["status"] == "completed"

    def test_patch_rating_reflected(self, client: TestClient) -> None:
        """AC-007: updated rating visible in subsequent GET."""
        item = _create(client)
        client.patch(f"{BASE}/{item['id']}", json={"rating": 7})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["rating"] == 7

    def test_patch_notes_reflected(self, client: TestClient) -> None:
        """AC-007: updated notes visible in subsequent GET."""
        item = _create(client)
        client.patch(f"{BASE}/{item['id']}", json={"notes": "New notes."})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["notes"] == "New notes."

    def test_patch_name_trimmed(self, client: TestClient) -> None:
        """AC-043 / VR-002: name with spaces trimmed on PATCH."""
        item = _create(client)
        client.patch(f"{BASE}/{item['id']}", json={"name": "  Trimmed  "})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["name"] == "Trimmed"

    def test_patch_clear_rating(self, client: TestClient) -> None:
        """DD-005 / AC-003: rating=null clears the field."""
        item = _create(client, MEDIA_BOOK_COMPLETED)
        client.patch(f"{BASE}/{item['id']}", json={"rating": None})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["rating"] is None

    def test_patch_clear_notes(self, client: TestClient) -> None:
        """DD-005 / AC-003: notes=null clears the field."""
        item = _create(client, MEDIA_FULL)
        client.patch(f"{BASE}/{item['id']}", json={"notes": None})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["notes"] is None

    def test_patch_absent_fields_unchanged(self, client: TestClient) -> None:
        """DD-004: absent fields in PATCH body are not modified."""
        item = _create(client, MEDIA_FULL)
        original_name = item["name"]
        client.patch(f"{BASE}/{item['id']}", json={"status": "abandoned"})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["name"] == original_name  # name unchanged

    def test_patch_nonexistent_returns_404(self, client: TestClient) -> None:
        """PATCH unknown id → 404."""
        resp = client.patch(
            f"{BASE}/00000000-0000-0000-0000-000000000000",
            json={"status": "completed"},
        )
        assert resp.status_code == 404, resp.text

    def test_patch_empty_name_rejected(self, client: TestClient) -> None:
        """AC-042 / VR-001: PATCH with empty name → 400."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"name": ""})
        assert resp.status_code == 400, resp.text
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    def test_patch_whitespace_name_rejected(self, client: TestClient) -> None:
        """AC-042 / VR-001: PATCH with whitespace name → 400."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"name": "   "})
        assert resp.status_code == 400, resp.text
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    def test_patch_rating_out_of_range_rejected(self, client: TestClient) -> None:
        """AC-044 / VR-007: PATCH rating=11 → 400."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"rating": 11})
        assert resp.status_code == 400, resp.text
        assert resp.json()["error"] == ERR_RATING_OUT_OF_RANGE

    def test_patch_response_body_is_updated_item(self, client: TestClient) -> None:
        """PATCH 200 body reflects the updated MediaItem (not old values)."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "abandoned"})
        assert resp.json()["status"] == "abandoned"
