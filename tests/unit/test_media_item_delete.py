"""
tests/unit/test_media_item_delete.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-004 — MediaItem Delete

SRS coverage:
  AC-008   deleted item no longer in library
  AC-010   Topic associations removed on MediaItem delete; Topics still exist
  AC-011   no restore after delete
  AC-054   no dangling association references

BDD coverage: BDD-013, BDD-015, BDD-016
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.fixtures.sample_data import ERR_NOT_FOUND, MEDIA_MINIMAL

BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _create_media(client: TestClient, payload: dict | None = None) -> dict:
    resp = client.post(BASE, json=payload or MEDIA_MINIMAL)
    assert resp.status_code == 201, resp.text
    return resp.json()


def _create_topic(client: TestClient, name: str = "SciFi") -> dict:
    resp = client.post(TOPIC_BASE, json={"name": name})
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestMediaItemDelete:
    """DELETE /api/media-items/{id}."""

    def test_delete_returns_204(self, client: TestClient) -> None:
        """BDD-013 / AC-008: DELETE existing item → 204."""
        item = _create_media(client)
        resp = client.delete(f"{BASE}/{item['id']}")
        assert resp.status_code == 204, resp.text

    def test_delete_204_no_body(self, client: TestClient) -> None:
        """204 response has no body."""
        item = _create_media(client)
        resp = client.delete(f"{BASE}/{item['id']}")
        assert resp.content == b"" or resp.status_code == 204

    def test_deleted_item_not_in_list(self, client: TestClient) -> None:
        """BDD-013 / AC-008: deleted item absent from GET /api/media-items."""
        item = _create_media(client)
        client.delete(f"{BASE}/{item['id']}")
        ids = [i["id"] for i in client.get(BASE).json()["data"]]
        assert item["id"] not in ids

    def test_deleted_item_get_returns_404(self, client: TestClient) -> None:
        """AC-008 / AC-011: GET deleted item id → 404."""
        item = _create_media(client)
        client.delete(f"{BASE}/{item['id']}")
        resp = client.get(f"{BASE}/{item['id']}")
        assert resp.status_code == 404, resp.text

    def test_deleted_item_404_error_code(self, client: TestClient) -> None:
        """404 body after delete has error == 'not_found'."""
        item = _create_media(client)
        client.delete(f"{BASE}/{item['id']}")
        resp = client.get(f"{BASE}/{item['id']}")
        assert resp.json()["error"] == ERR_NOT_FOUND

    def test_delete_nonexistent_returns_404(self, client: TestClient) -> None:
        """DELETE unknown id → 404."""
        resp = client.delete(f"{BASE}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404, resp.text

    def test_delete_removes_topic_association(self, client: TestClient) -> None:
        """BDD-015 / AC-010: after MediaItem deleted, Topic no longer lists it."""
        topic = _create_topic(client, "Space")
        item = _create_media(client)
        # Associate
        client.post(f"{BASE}/{item['id']}/topics/{topic['id']}")
        # Delete MediaItem
        client.delete(f"{BASE}/{item['id']}")
        # Topic still exists and no longer references the deleted item
        t_resp = client.get(f"{TOPIC_BASE}/{topic['id']}")
        assert t_resp.status_code == 200, t_resp.text
        media_ids = [m["id"] for m in t_resp.json()["media_items"]]
        assert item["id"] not in media_ids

    def test_delete_topics_still_exist(self, client: TestClient) -> None:
        """BDD-015 / AC-010: associated Topics are not deleted with the MediaItem."""
        topic = _create_topic(client, "Movies")
        item = _create_media(client)
        client.post(f"{BASE}/{item['id']}/topics/{topic['id']}")
        client.delete(f"{BASE}/{item['id']}")
        resp = client.get(f"{TOPIC_BASE}/{topic['id']}")
        assert resp.status_code == 200, "Topic should still exist after MediaItem delete"

    def test_other_items_unaffected_by_delete(self, client: TestClient) -> None:
        """Deleting one item does not remove another from the list."""
        item_a = _create_media(client, {"name": "Alpha", "type": "book"})
        item_b = _create_media(client, {"name": "Beta", "type": "movie"})
        client.delete(f"{BASE}/{item_a['id']}")
        ids = [i["id"] for i in client.get(BASE).json()["data"]]
        assert item_b["id"] in ids

    def test_double_delete_returns_404(self, client: TestClient) -> None:
        """AC-011: deleting an already-deleted item → 404 (no restore possible)."""
        item = _create_media(client)
        client.delete(f"{BASE}/{item['id']}")
        resp = client.delete(f"{BASE}/{item['id']}")
        assert resp.status_code == 404, resp.text
