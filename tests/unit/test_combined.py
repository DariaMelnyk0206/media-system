"""
tests/unit/test_combined.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-013 — Combined Search + Filter + Sort

SRS coverage:
  AC-041  search + filter + sort simultaneously → AND logic + order

BDD coverage: BDD-052 (via sort), BDD-041 (via empty search), BDD-051 (via AND)
"""

from __future__ import annotations

from fastapi.testclient import TestClient

MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _m(client: TestClient, name: str, mtype: str = "book",
        status: str = "planned", rating: int | None = None) -> dict:
    payload: dict = {"name": name, "type": mtype, "status": status}
    if rating is not None:
        payload["rating"] = rating
    r = client.post(MEDIA_BASE, json=payload)
    assert r.status_code == 201, r.text
    return r.json()


class TestCombined:
    """AC-041 / BDD-057 (combined ops)."""

    def test_search_plus_type_filter(self, client: TestClient) -> None:
        """Search 'cosmos' AND type=book → only book named Cosmos."""
        _m(client, "Cosmos", mtype="book")
        _m(client, "Cosmos Movie", mtype="movie")
        resp = client.get(MEDIA_BASE, params={"q": "cosmos", "type": "book"})
        items = resp.json()["data"]
        assert all(i["type"] == "book" for i in items)
        assert all("cosmos" in i["name"].lower() for i in items)

    def test_search_plus_status_filter(self, client: TestClient) -> None:
        """Search 'book' AND status=completed → only matching item."""
        _m(client, "Good Book", mtype="book", status="completed")
        _m(client, "Planned Book", mtype="book", status="planned")
        resp = client.get(MEDIA_BASE, params={"q": "Book", "status": "completed"})
        items = resp.json()["data"]
        assert len(items) == 1
        assert items[0]["name"] == "Good Book"

    def test_search_plus_rating_filter(self, client: TestClient) -> None:
        """Search 'star' AND rating_min=8 → only highly-rated items."""
        _m(client, "Stardust", rating=9)
        _m(client, "Stargate", rating=5)
        _m(client, "Unrated Star")
        resp = client.get(MEDIA_BASE, params={"q": "star", "rating_min": 8})
        items = resp.json()["data"]
        assert all("star" in i["name"].lower() for i in items)
        assert all(i["rating"] is not None and i["rating"] >= 8 for i in items)

    def test_filter_plus_sort(self, client: TestClient) -> None:
        """Filter type=book AND sort by name asc."""
        _m(client, "Zebra Book", mtype="book")
        _m(client, "Alpha Book", mtype="book")
        _m(client, "Alpha Movie", mtype="movie")
        resp = client.get(MEDIA_BASE, params={"type": "book", "sort": "name", "dir": "asc"})
        items = resp.json()["data"]
        assert all(i["type"] == "book" for i in items)
        names = [i["name"] for i in items]
        assert names.index("Alpha Book") < names.index("Zebra Book")

    def test_search_filter_sort_combined(self, client: TestClient) -> None:
        """AC-041: search + filter + sort all active simultaneously."""
        _m(client, "Space Adventure", mtype="movie", status="completed", rating=8)
        _m(client, "Space History", mtype="movie", status="completed", rating=6)
        _m(client, "Space Epic", mtype="book", status="completed", rating=9)
        _m(client, "Ocean Blue", mtype="movie", status="completed", rating=7)
        resp = client.get(MEDIA_BASE, params={
            "q": "space",
            "type": "movie",
            "status": "completed",
            "sort": "rating",
            "dir": "desc",
        })
        items = resp.json()["data"]
        # Only "Space Adventure" and "Space History" match (space + movie + completed)
        names = [i["name"] for i in items]
        assert "Space Adventure" in names
        assert "Space History" in names
        assert "Space Epic" not in names   # type=book excluded
        assert "Ocean Blue" not in names   # search "space" excluded
        # Sorted by rating desc: Adventure(8) before History(6)
        assert names.index("Space Adventure") < names.index("Space History")

    def test_empty_search_with_filter(self, client: TestClient) -> None:
        """AC-027 + AC-036: empty q doesn't restrict, filter still applied."""
        _m(client, "Book A", mtype="book")
        _m(client, "Movie A", mtype="movie")
        resp = client.get(MEDIA_BASE, params={"q": "", "type": "book"})
        items = resp.json()["data"]
        assert all(i["type"] == "book" for i in items)

    def test_no_results_all_active(self, client: TestClient) -> None:
        """When no item satisfies all constraints → empty list (AC-036)."""
        _m(client, "Cosmos", mtype="book", status="planned")
        resp = client.get(MEDIA_BASE, params={
            "q": "cosmos",
            "type": "movie",
            "status": "completed",
        })
        assert resp.json()["data"] == []
