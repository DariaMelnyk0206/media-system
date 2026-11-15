"""
tests/unit/test_topic_crud.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-006 — Topic CRUD (позитивні)
TEST-007 — Topic Validation (негативні)

SRS coverage:
  AC-013  create topic → 201, present in library
  AC-014  view topic with/without media items
  AC-015  rename topic, associations preserved
  AC-016  delete topic → Topics removed, MediaItems intact
  AC-045  empty/whitespace name rejected (VR-003)
  AC-046  duplicate name rejected case-insensitively (VR-005, 409)
  AC-047  topic name trimmed (VR-004)

BDD coverage: BDD-018..029
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import (
    ERR_NAME_REQUIRED,
    ERR_NAME_TAKEN,
    ERR_NOT_FOUND,
    FIELD_NAME,
    MEDIA_MINIMAL,
    TOPIC_EMPTY_NAME,
    TOPIC_PADDED_NAME,
    TOPIC_PADDED_NAME_EXPECTED,
    TOPIC_SCI_FI,
    TOPIC_WHITESPACE_NAME,
)

TOPIC_BASE = "/api/topics"
MEDIA_BASE = "/api/media-items"


def _create_topic(client: TestClient, name: str = "SciFi") -> dict:
    resp = client.post(TOPIC_BASE, json={"name": name})
    assert resp.status_code == 201, resp.text
    return resp.json()


def _create_media(client: TestClient, name: str = "Dune") -> dict:
    resp = client.post(MEDIA_BASE, json={"name": name, "type": "book"})
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# TEST-006  CRUD positive
# ---------------------------------------------------------------------------


class TestTopicCrudPositive:
    """TEST-006: Topic create / read / update / delete — happy paths."""

    # --- Create ---

    def test_create_returns_201(self, client: TestClient) -> None:
        """BDD-018 / AC-013: POST /api/topics → 201."""
        resp = client.post(TOPIC_BASE, json=TOPIC_SCI_FI)
        assert resp.status_code == 201, resp.text

    def test_create_response_shape(self, client: TestClient) -> None:
        """AC-013: response has id, name, media_items."""
        resp = client.post(TOPIC_BASE, json=TOPIC_SCI_FI)
        body = resp.json()
        for field in ("id", "name", "media_items"):
            assert field in body, f"Missing field: {field}"

    def test_create_name_stored(self, client: TestClient) -> None:
        """AC-013: stored name matches submitted name."""
        resp = client.post(TOPIC_BASE, json=TOPIC_SCI_FI)
        assert resp.json()["name"] == TOPIC_SCI_FI["name"]

    def test_create_media_items_empty_on_new(self, client: TestClient) -> None:
        """AC-014: new topic has empty media_items list."""
        resp = client.post(TOPIC_BASE, json=TOPIC_SCI_FI)
        assert resp.json()["media_items"] == []

    def test_create_name_is_trimmed(self, client: TestClient) -> None:
        """BDD-022 / AC-047 / VR-004: name trimmed before saving."""
        resp = client.post(TOPIC_BASE, json=TOPIC_PADDED_NAME)
        assert resp.status_code == 201
        assert resp.json()["name"] == TOPIC_PADDED_NAME_EXPECTED

    # --- List ---

    def test_list_topics_returns_200(self, client: TestClient) -> None:
        """GET /api/topics → 200."""
        resp = client.get(TOPIC_BASE)
        assert resp.status_code == 200, resp.text

    def test_list_topics_shape(self, client: TestClient) -> None:
        """GET /api/topics body has 'data' list."""
        resp = client.get(TOPIC_BASE)
        body = resp.json()
        assert "data" in body
        assert isinstance(body["data"], list)

    def test_list_includes_created_topic(self, client: TestClient) -> None:
        """Created topic appears in list."""
        t = _create_topic(client, "History")
        ids = [item["id"] for item in client.get(TOPIC_BASE).json()["data"]]
        assert t["id"] in ids

    # --- Get single ---

    def test_get_topic_returns_200(self, client: TestClient) -> None:
        """BDD-023 / AC-014: GET /api/topics/{id} → 200."""
        t = _create_topic(client)
        resp = client.get(f"{TOPIC_BASE}/{t['id']}")
        assert resp.status_code == 200, resp.text

    def test_get_topic_with_media_items(self, client: TestClient) -> None:
        """BDD-023 / AC-014: associated MediaItems shown in Topic response."""
        t = _create_topic(client, "Space")
        m = _create_media(client, "The Martian")
        # Associate from media side
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        ids = [mi["id"] for mi in body["media_items"]]
        assert m["id"] in ids

    def test_get_empty_topic(self, client: TestClient) -> None:
        """BDD-024 / AC-014: topic with no media shows empty list."""
        t = _create_topic(client, "Unassigned")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert body["media_items"] == []

    def test_get_nonexistent_topic_404(self, client: TestClient) -> None:
        """GET unknown topic id → 404."""
        resp = client.get(f"{TOPIC_BASE}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404, resp.text
        assert resp.json()["error"] == ERR_NOT_FOUND

    # --- Rename (PATCH) ---

    def test_rename_returns_200(self, client: TestClient) -> None:
        """BDD-025 / AC-015: PATCH /api/topics/{id} → 200."""
        t = _create_topic(client, "Sci-Fi")
        resp = client.patch(f"{TOPIC_BASE}/{t['id']}", json={"name": "Science Fiction"})
        assert resp.status_code == 200, resp.text

    def test_rename_name_updated(self, client: TestClient) -> None:
        """AC-015: new name reflected in response and subsequent GET."""
        t = _create_topic(client, "Sci-Fi")
        client.patch(f"{TOPIC_BASE}/{t['id']}", json={"name": "Science Fiction"})
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert body["name"] == "Science Fiction"

    def test_rename_preserves_associations(self, client: TestClient) -> None:
        """BDD-025 / AC-015: associated MediaItems preserved after rename."""
        t = _create_topic(client, "Sci-Fi")
        m = _create_media(client, "Dune")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        client.patch(f"{TOPIC_BASE}/{t['id']}", json={"name": "Science Fiction"})
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        ids = [mi["id"] for mi in body["media_items"]]
        assert m["id"] in ids

    def test_rename_nonexistent_404(self, client: TestClient) -> None:
        """PATCH unknown topic → 404."""
        resp = client.patch(
            f"{TOPIC_BASE}/00000000-0000-0000-0000-000000000000",
            json={"name": "New Name"},
        )
        assert resp.status_code == 404, resp.text

    # --- Delete ---

    def test_delete_returns_204(self, client: TestClient) -> None:
        """BDD-027 / AC-016: DELETE /api/topics/{id} → 204."""
        t = _create_topic(client)
        resp = client.delete(f"{TOPIC_BASE}/{t['id']}")
        assert resp.status_code == 204, resp.text

    def test_deleted_topic_404_on_get(self, client: TestClient) -> None:
        """AC-016: GET deleted topic → 404."""
        t = _create_topic(client)
        client.delete(f"{TOPIC_BASE}/{t['id']}")
        resp = client.get(f"{TOPIC_BASE}/{t['id']}")
        assert resp.status_code == 404

    def test_delete_topic_media_items_intact(self, client: TestClient) -> None:
        """BDD-029 / AC-016: MediaItems still exist after Topic deleted."""
        t = _create_topic(client, "Drama")
        m1 = _create_media(client, "Roma")
        m2 = _create_media(client, "Parasite")
        client.post(f"{MEDIA_BASE}/{m1['id']}/topics/{t['id']}")
        client.post(f"{MEDIA_BASE}/{m2['id']}/topics/{t['id']}")
        client.delete(f"{TOPIC_BASE}/{t['id']}")
        for m_id in (m1["id"], m2["id"]):
            assert client.get(f"{MEDIA_BASE}/{m_id}").status_code == 200

    def test_delete_nonexistent_topic_404(self, client: TestClient) -> None:
        """DELETE unknown topic id → 404."""
        resp = client.delete(f"{TOPIC_BASE}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404, resp.text


# ---------------------------------------------------------------------------
# TEST-007  Validation negative
# ---------------------------------------------------------------------------


class TestTopicValidation:
    """TEST-007: Topic name validation (VR-003..006)."""

    # --- VR-003: empty name ---

    def test_empty_name_rejected_400(self, client: TestClient) -> None:
        """BDD-019 / AC-045 / VR-003: empty name → 400."""
        resp = client.post(TOPIC_BASE, json=TOPIC_EMPTY_NAME)
        assert resp.status_code == 400, resp.text

    def test_empty_name_error_code(self, client: TestClient) -> None:
        """BDD-019 / AC-045: error.error == 'name_required'."""
        resp = client.post(TOPIC_BASE, json=TOPIC_EMPTY_NAME)
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    def test_empty_name_error_field(self, client: TestClient) -> None:
        """BDD-019 / AC-045: error.field == 'name'."""
        resp = client.post(TOPIC_BASE, json=TOPIC_EMPTY_NAME)
        assert resp.json()["field"] == FIELD_NAME

    def test_whitespace_name_rejected_400(self, client: TestClient) -> None:
        """VR-003: whitespace-only topic name → 400."""
        resp = client.post(TOPIC_BASE, json=TOPIC_WHITESPACE_NAME)
        assert resp.status_code == 400, resp.text

    def test_whitespace_name_error_code(self, client: TestClient) -> None:
        """VR-003: error.error == 'name_required'."""
        resp = client.post(TOPIC_BASE, json=TOPIC_WHITESPACE_NAME)
        assert resp.json()["error"] == ERR_NAME_REQUIRED

    # --- VR-005: duplicate name case-insensitive → 409 ---

    def test_duplicate_name_exact_409(self, client: TestClient) -> None:
        """BDD-020 / AC-046 / VR-005: exact duplicate → 409."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "Science"})
        assert resp.status_code == 409, resp.text

    def test_duplicate_name_lowercase_409(self, client: TestClient) -> None:
        """BDD-020 / AC-046 / VR-005: lowercase duplicate → 409."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "science"})
        assert resp.status_code == 409, resp.text

    def test_duplicate_name_uppercase_409(self, client: TestClient) -> None:
        """BDD-020 / AC-046 / VR-005: uppercase duplicate → 409."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "SCIENCE"})
        assert resp.status_code == 409, resp.text

    def test_duplicate_name_with_spaces_409(self, client: TestClient) -> None:
        """BDD-021 / AC-046 / VR-005..006: padded duplicate → 409."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "  Science  "})
        assert resp.status_code == 409, resp.text

    def test_duplicate_name_error_code(self, client: TestClient) -> None:
        """AC-046: error.error == 'name_taken'."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "Science"})
        assert resp.json()["error"] == ERR_NAME_TAKEN

    def test_duplicate_name_error_field(self, client: TestClient) -> None:
        """AC-046: error.field == 'name'."""
        _create_topic(client, "Science")
        resp = client.post(TOPIC_BASE, json={"name": "Science"})
        assert resp.json()["field"] == FIELD_NAME

    # --- VR-006: rename to duplicate → 409 ---

    def test_rename_to_existing_name_409(self, client: TestClient) -> None:
        """BDD-026 / AC-046 / VR-006: rename to existing topic name → 409."""
        _create_topic(client, "Science")
        t2 = _create_topic(client, "History")
        resp = client.patch(f"{TOPIC_BASE}/{t2['id']}", json={"name": "science"})
        assert resp.status_code == 409, resp.text

    def test_rename_to_existing_name_error_code(self, client: TestClient) -> None:
        """VR-006: rename conflict error.error == 'name_taken'."""
        _create_topic(client, "Science")
        t2 = _create_topic(client, "History")
        resp = client.patch(f"{TOPIC_BASE}/{t2['id']}", json={"name": "science"})
        assert resp.json()["error"] == ERR_NAME_TAKEN

    def test_rename_to_own_name_allowed(self, client: TestClient) -> None:
        """VR-006 edge case: renaming to same name (case-identical) should not 409."""
        t = _create_topic(client, "History")
        resp = client.patch(f"{TOPIC_BASE}/{t['id']}", json={"name": "History"})
        # Identical rename to self should succeed (200) — not a conflict
        assert resp.status_code == 200, resp.text

    def test_rename_empty_name_rejected(self, client: TestClient) -> None:
        """VR-003: rename to empty name → 400."""
        t = _create_topic(client)
        resp = client.patch(f"{TOPIC_BASE}/{t['id']}", json={"name": ""})
        assert resp.status_code == 400, resp.text
        assert resp.json()["error"] == ERR_NAME_REQUIRED
