"""
tests/unit/test_media_item_status.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-005 — MediaItem Status Management

SRS coverage:
  AC-012   status can change to any of 5 values from any other (BR-010)
  AC-065   invalid status rejected (VR-009)

BDD coverage: BDD-017a, BDD-017b
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import ERR_INVALID_STATUS, FIELD_STATUS, MEDIA_MINIMAL

BASE = "/api/media-items"
ALL_STATUSES = ["planned", "in_progress", "postponed", "abandoned", "completed"]


def _create(client: TestClient, status: str = "planned") -> dict:
    payload = {**MEDIA_MINIMAL, "status": status}
    resp = client.post(BASE, json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestMediaItemStatus:
    """Status lifecycle: any → any (BR-010, no sequence restrictions)."""

    def test_default_status_planned(self, client: TestClient) -> None:
        """AC-002 / AC-060: freshly created item has status 'planned'."""
        item = _create(client)
        assert item["status"] == "planned"

    @pytest.mark.parametrize("target", ALL_STATUSES)
    def test_change_status_from_planned(
        self, client: TestClient, target: str
    ) -> None:
        """BDD-017a / AC-012: planned → any status."""
        item = _create(client, "planned")
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": target})
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == target

    @pytest.mark.parametrize("source", ALL_STATUSES)
    def test_change_status_from_any_to_completed(
        self, client: TestClient, source: str
    ) -> None:
        """BDD-017b / AC-012: any → completed allowed."""
        item = _create(client, source)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "completed"})
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == "completed"

    @pytest.mark.parametrize("source", ALL_STATUSES)
    @pytest.mark.parametrize("target", ALL_STATUSES)
    def test_all_status_transitions_allowed(
        self, client: TestClient, source: str, target: str
    ) -> None:
        """AC-012 / BR-010: every status → every status is permitted."""
        item = _create(client, source)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": target})
        assert resp.status_code == 200, (
            f"Transition {source!r} → {target!r} failed: {resp.text}"
        )
        assert resp.json()["status"] == target

    def test_status_persisted_in_get(self, client: TestClient) -> None:
        """AC-007: changed status visible on subsequent GET."""
        item = _create(client, "planned")
        client.patch(f"{BASE}/{item['id']}", json={"status": "abandoned"})
        body = client.get(f"{BASE}/{item['id']}").json()
        assert body["status"] == "abandoned"

    def test_invalid_status_rejected(self, client: TestClient) -> None:
        """AC-065 / VR-009: invalid status string → 400."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "watching"})
        assert resp.status_code == 400, resp.text

    def test_invalid_status_error_code(self, client: TestClient) -> None:
        """VR-009: error.error == 'invalid_status'."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "unknown"})
        assert resp.json()["error"] == ERR_INVALID_STATUS

    def test_invalid_status_error_field(self, client: TestClient) -> None:
        """VR-009: error.field == 'status'."""
        item = _create(client)
        resp = client.patch(f"{BASE}/{item['id']}", json={"status": "unknown"})
        assert resp.json()["field"] == FIELD_STATUS

    def test_status_in_list_response(self, client: TestClient) -> None:
        """AC-012: changed status reflected in list."""
        item = _create(client, "planned")
        client.patch(f"{BASE}/{item['id']}", json={"status": "in_progress"})
        items = client.get(BASE).json()["data"]
        matched = next((i for i in items if i["id"] == item["id"]), None)
        assert matched is not None
        assert matched["status"] == "in_progress"
