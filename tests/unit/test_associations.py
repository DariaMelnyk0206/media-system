"""
tests/unit/test_associations.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-008 — MediaItem–Topic Association (обидві сторони)
TEST-009 — Navigation Topic↔MediaItem

SRS coverage:
  AC-018  add/remove Topic from MediaItem side
  AC-019  add/remove MediaItem from Topic side
  AC-020  association persists (at least within session)
  AC-021  navigate from Topic → MediaItem details
  AC-022  navigate from MediaItem → Topic details
  AC-054  no dangling references after removal

BDD coverage: BDD-030..036
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.fixtures.sample_data import ERR_NOT_FOUND, MEDIA_MINIMAL

MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _media(client: TestClient, name: str = "Dune") -> dict:
    r = client.post(MEDIA_BASE, json={"name": name, "type": "book"})
    assert r.status_code == 201, r.text
    return r.json()


def _topic(client: TestClient, name: str = "SciFi") -> dict:
    r = client.post(TOPIC_BASE, json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()


# ---------------------------------------------------------------------------
# TEST-008  Association operations
# ---------------------------------------------------------------------------


class TestAssociationMediaItemSide:
    """POST/DELETE /api/media-items/{id}/topics/{topicId}."""

    def test_add_topic_to_media_returns_200(self, client: TestClient) -> None:
        """BDD-030 / AC-018: POST association → 200."""
        m, t = _media(client), _topic(client)
        resp = client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        assert resp.status_code == 200, resp.text

    def test_add_topic_reflected_in_media_response(self, client: TestClient) -> None:
        """BDD-030 / AC-018: MediaItem response body shows Topic."""
        m, t = _media(client), _topic(client)
        resp = client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        topic_ids = [tp["id"] for tp in resp.json()["topics"]]
        assert t["id"] in topic_ids

    def test_add_topic_reflected_in_get(self, client: TestClient) -> None:
        """AC-018: association visible in subsequent GET /media-items/{id}."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert any(tp["id"] == t["id"] for tp in body["topics"])

    def test_add_topic_reflected_in_topic_get(self, client: TestClient) -> None:
        """BDD-030 / AC-018: Topic's media_items also shows the MediaItem."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert any(mi["id"] == m["id"] for mi in body["media_items"])

    def test_add_topic_idempotent(self, client: TestClient) -> None:
        """DD-006: second POST to same association → 200 (idempotent)."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        resp = client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        assert resp.status_code == 200, resp.text

    def test_add_topic_idempotent_no_duplicate(self, client: TestClient) -> None:
        """DD-006: duplicate POST doesn't create duplicate entry in topics list."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        matching = [tp for tp in body["topics"] if tp["id"] == t["id"]]
        assert len(matching) == 1

    def test_add_topic_nonexistent_media_404(self, client: TestClient) -> None:
        """AC-018: POST with unknown mediaId → 404."""
        t = _topic(client)
        resp = client.post(
            f"{MEDIA_BASE}/00000000-0000-0000-0000-000000000000/topics/{t['id']}"
        )
        assert resp.status_code == 404, resp.text
        assert resp.json()["error"] == ERR_NOT_FOUND

    def test_add_topic_nonexistent_topic_404(self, client: TestClient) -> None:
        """AC-018: POST with unknown topicId → 404."""
        m = _media(client)
        resp = client.post(
            f"{MEDIA_BASE}/{m['id']}/topics/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404, resp.text

    def test_remove_topic_returns_204(self, client: TestClient) -> None:
        """AC-018: DELETE association → 204."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        resp = client.delete(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        assert resp.status_code == 204, resp.text

    def test_remove_topic_no_longer_in_media(self, client: TestClient) -> None:
        """BDD-031 / AC-018: removed Topic absent from MediaItem."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        client.delete(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert all(tp["id"] != t["id"] for tp in body["topics"])

    def test_remove_topic_no_longer_in_topic(self, client: TestClient) -> None:
        """BDD-031 / AC-018: removed MediaItem absent from Topic's list."""
        m, t = _media(client), _topic(client)
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        client.delete(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert all(mi["id"] != m["id"] for mi in body["media_items"])

    def test_remove_nonexistent_association_404(self, client: TestClient) -> None:
        """AC-018: DELETE non-existing association → 404."""
        m, t = _media(client), _topic(client)
        resp = client.delete(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        assert resp.status_code == 404, resp.text


class TestAssociationTopicSide:
    """POST/DELETE /api/topics/{id}/media-items/{mediaId}."""

    def test_add_media_to_topic_returns_200(self, client: TestClient) -> None:
        """BDD-032 / AC-019: POST from Topic side → 200."""
        m, t = _media(client), _topic(client)
        resp = client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        assert resp.status_code == 200, resp.text

    def test_add_media_reflected_in_topic_response(self, client: TestClient) -> None:
        """BDD-032 / AC-019: Topic response body shows MediaItem."""
        m, t = _media(client), _topic(client)
        resp = client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        ids = [mi["id"] for mi in resp.json()["media_items"]]
        assert m["id"] in ids

    def test_add_media_reflected_in_media_get(self, client: TestClient) -> None:
        """BDD-032 / AC-019: MediaItem's topics also shows the Topic."""
        m, t = _media(client), _topic(client)
        client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert any(tp["id"] == t["id"] for tp in body["topics"])

    def test_add_media_idempotent(self, client: TestClient) -> None:
        """DD-006: second POST from Topic side → 200 (idempotent)."""
        m, t = _media(client), _topic(client)
        client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        resp = client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        assert resp.status_code == 200, resp.text

    def test_add_media_nonexistent_topic_404(self, client: TestClient) -> None:
        """AC-019: POST with unknown topicId → 404."""
        m = _media(client)
        resp = client.post(
            f"{TOPIC_BASE}/00000000-0000-0000-0000-000000000000/media-items/{m['id']}"
        )
        assert resp.status_code == 404, resp.text

    def test_add_media_nonexistent_media_404(self, client: TestClient) -> None:
        """AC-019: POST with unknown mediaId → 404."""
        t = _topic(client)
        resp = client.post(
            f"{TOPIC_BASE}/{t['id']}/media-items/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404, resp.text

    def test_remove_media_from_topic_returns_204(self, client: TestClient) -> None:
        """BDD-033 / AC-019: DELETE from Topic side → 204."""
        m, t = _media(client), _topic(client)
        client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        resp = client.delete(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        assert resp.status_code == 204, resp.text

    def test_remove_media_no_longer_in_topic(self, client: TestClient) -> None:
        """BDD-033 / AC-019: removed MediaItem absent from Topic."""
        m, t = _media(client), _topic(client)
        client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        client.delete(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert all(mi["id"] != m["id"] for mi in body["media_items"])

    def test_remove_media_no_longer_in_media_topics(self, client: TestClient) -> None:
        """BDD-033 / AC-019: removed Topic absent from MediaItem's topics."""
        m, t = _media(client), _topic(client)
        client.post(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        client.delete(f"{TOPIC_BASE}/{t['id']}/media-items/{m['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert all(tp["id"] != t["id"] for tp in body["topics"])


# ---------------------------------------------------------------------------
# TEST-009  Navigation
# ---------------------------------------------------------------------------


class TestNavigation:
    """TEST-009: bi-directional navigation between Topics and MediaItems."""

    def test_navigate_topic_to_media(self, client: TestClient) -> None:
        """BDD-035 / AC-021: Topic response lists associated MediaItem by id."""
        t = _topic(client, "Space")
        m = _media(client, "The Martian")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        assert any(mi["id"] == m["id"] for mi in body["media_items"])

    def test_navigate_topic_to_media_full_detail(self, client: TestClient) -> None:
        """AC-021: MediaItemRef in Topic has id, name, type, status."""
        t = _topic(client, "Space")
        m = _media(client, "Gravity")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        ref = next(mi for mi in body["media_items"] if mi["id"] == m["id"])
        for field in ("id", "name", "type", "status"):
            assert field in ref, f"MediaItemRef missing field: {field}"

    def test_navigate_media_to_topic(self, client: TestClient) -> None:
        """BDD-036 / AC-022: MediaItem response lists associated Topic by id."""
        t = _topic(client, "Science Fiction")
        m = _media(client, "Interstellar")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert any(tp["id"] == t["id"] for tp in body["topics"])

    def test_navigate_media_to_topic_name_present(self, client: TestClient) -> None:
        """AC-022: TopicRef in MediaItem has id and name."""
        t = _topic(client, "Science Fiction")
        m = _media(client, "Interstellar")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        ref = next(tp for tp in body["topics"] if tp["id"] == t["id"])
        assert ref["name"] == "Science Fiction"

    def test_multiple_topics_navigable_from_media(self, client: TestClient) -> None:
        """AC-022: MediaItem with multiple Topics lists all of them."""
        t1 = _topic(client, "Space")
        t2 = _topic(client, "Drama")
        m = _media(client, "Gravity")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t1['id']}")
        client.post(f"{MEDIA_BASE}/{m['id']}/topics/{t2['id']}")
        body = client.get(f"{MEDIA_BASE}/{m['id']}").json()
        ids = [tp["id"] for tp in body["topics"]]
        assert t1["id"] in ids
        assert t2["id"] in ids

    def test_multiple_media_navigable_from_topic(self, client: TestClient) -> None:
        """AC-021: Topic with multiple MediaItems lists all of them."""
        t = _topic(client, "Space")
        m1 = _media(client, "Interstellar")
        m2 = _media(client, "Gravity")
        client.post(f"{MEDIA_BASE}/{m1['id']}/topics/{t['id']}")
        client.post(f"{MEDIA_BASE}/{m2['id']}/topics/{t['id']}")
        body = client.get(f"{TOPIC_BASE}/{t['id']}").json()
        ids = [mi["id"] for mi in body["media_items"]]
        assert m1["id"] in ids
        assert m2["id"] in ids
