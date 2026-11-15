"""
tests/unit/test_filter.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-011 — Filter (GET /api/media-items with filter params)

SRS coverage:
  AC-029  type filter
  AC-030  status filter
  AC-031  rating_min only
  AC-032  rating_max only
  AC-033  rating both bounds
  AC-034  unrated items excluded when any rating filter active
  AC-035  topic_id filter
  AC-036  AND logic for combined filters
  AC-048  invalid_rating_range if min > max (VR-010)

BDD coverage: BDD-043..051
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import ERR_INVALID_RATING_RANGE, FIELD_RATING_MIN

MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _m(client: TestClient, **kwargs) -> dict:
    payload = {"name": kwargs.pop("name"), "type": kwargs.pop("type_", "book"), **kwargs}
    r = client.post(MEDIA_BASE, json=payload)
    assert r.status_code == 201, r.text
    return r.json()


def _t(client: TestClient, name: str) -> dict:
    r = client.post(TOPIC_BASE, json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()


def _list(client: TestClient, **params) -> list[dict]:
    return client.get(MEDIA_BASE, params=params).json()["data"]


class TestFilterByType:
    """AC-029 / BDD-043: type filter."""

    def test_type_filter_returns_only_books(self, client: TestClient) -> None:
        _m(client, name="Book One", type_="book")
        _m(client, name="Movie One", type_="movie")
        items = _list(client, type="book")
        assert all(i["type"] == "book" for i in items)

    def test_type_filter_excludes_other_types(self, client: TestClient) -> None:
        _m(client, name="Book One", type_="book")
        _m(client, name="Movie One", type_="movie")
        items = _list(client, type="book")
        assert not any(i["type"] == "movie" for i in items)

    def test_type_filter_empty_when_no_match(self, client: TestClient) -> None:
        _m(client, name="Book One", type_="book")
        items = _list(client, type="podcast")
        assert items == []

    @pytest.mark.parametrize(
        "mtype",
        ["book", "movie", "tv_series", "article", "podcast", "video", "other"],
    )
    def test_type_filter_all_valid_types(
        self, client: TestClient, mtype: str
    ) -> None:
        _m(client, name=f"Item {mtype}", type_=mtype)
        items = _list(client, type=mtype)
        assert len(items) >= 1
        assert all(i["type"] == mtype for i in items)


class TestFilterByStatus:
    """AC-030 / BDD-044: status filter."""

    def test_status_filter_returns_only_completed(self, client: TestClient) -> None:
        _m(client, name="Planned", type_="book", status="planned")
        _m(client, name="Done", type_="book", status="completed")
        items = _list(client, status="completed")
        assert all(i["status"] == "completed" for i in items)
        assert len(items) == 1

    def test_status_filter_excludes_others(self, client: TestClient) -> None:
        _m(client, name="Planned", type_="book", status="planned")
        _m(client, name="Done", type_="book", status="completed")
        items = _list(client, status="planned")
        assert not any(i["status"] == "completed" for i in items)


class TestFilterByRating:
    """AC-031..034 / BDD-045..047: rating filter."""

    def _setup(self, client: TestClient) -> None:
        _m(client, name="R5", type_="book", rating=5)
        _m(client, name="R7", type_="book", rating=7)
        _m(client, name="R9", type_="book", rating=9)
        _m(client, name="Unrated", type_="book")

    def test_rating_min_only(self, client: TestClient) -> None:
        """BDD-045 / AC-031: only items with rating >= 7 returned."""
        self._setup(client)
        items = _list(client, rating_min=7)
        ratings = [i["rating"] for i in items]
        assert all(r >= 7 for r in ratings)
        assert 5 not in ratings

    def test_rating_min_excludes_unrated(self, client: TestClient) -> None:
        """AC-034: unrated items absent when rating_min active."""
        self._setup(client)
        items = _list(client, rating_min=7)
        assert all(i["rating"] is not None for i in items)

    def test_rating_max_only(self, client: TestClient) -> None:
        """BDD-046 / AC-032: only items with rating <= 5 returned."""
        self._setup(client)
        items = _list(client, rating_max=5)
        ratings = [i["rating"] for i in items]
        assert all(r <= 5 for r in ratings)
        assert 7 not in ratings
        assert 9 not in ratings

    def test_rating_max_excludes_unrated(self, client: TestClient) -> None:
        """AC-034: unrated items absent when rating_max active."""
        self._setup(client)
        items = _list(client, rating_max=5)
        assert all(i["rating"] is not None for i in items)

    def test_rating_range_both_bounds(self, client: TestClient) -> None:
        """BDD-047 / AC-033: 4 <= rating <= 7 → only R5 and R7."""
        _m(client, name="R3", type_="book", rating=3)
        _m(client, name="R4", type_="book", rating=4)
        _m(client, name="R7b", type_="book", rating=7)
        _m(client, name="R8", type_="book", rating=8)
        _m(client, name="Unrated", type_="book")
        items = _list(client, rating_min=4, rating_max=7)
        ratings = [i["rating"] for i in items]
        assert all(4 <= r <= 7 for r in ratings)
        assert 3 not in ratings
        assert 8 not in ratings

    def test_rating_range_excludes_unrated(self, client: TestClient) -> None:
        """AC-034: unrated excluded even with both bounds."""
        self._setup(client)
        items = _list(client, rating_min=5, rating_max=9)
        assert all(i["rating"] is not None for i in items)

    def test_invalid_rating_range_rejected(self, client: TestClient) -> None:
        """BDD-048 / AC-048 / VR-010: rating_min > rating_max → 400."""
        resp = client.get(MEDIA_BASE, params={"rating_min": 8, "rating_max": 3})
        assert resp.status_code == 400, resp.text

    def test_invalid_rating_range_error_code(self, client: TestClient) -> None:
        """AC-048 / VR-010: error.error == 'invalid_rating_range'."""
        resp = client.get(MEDIA_BASE, params={"rating_min": 8, "rating_max": 3})
        assert resp.json()["error"] == ERR_INVALID_RATING_RANGE

    def test_invalid_rating_range_error_field(self, client: TestClient) -> None:
        """AC-048 / VR-010: error.field == 'rating_min'."""
        resp = client.get(MEDIA_BASE, params={"rating_min": 8, "rating_max": 3})
        assert resp.json()["field"] == FIELD_RATING_MIN


class TestFilterByTopic:
    """AC-035 / BDD-049..050: topic_id filter."""

    def test_topic_filter_returns_associated_items(self, client: TestClient) -> None:
        """BDD-049 / AC-035: only MediaItems associated with topic returned."""
        t = _t(client, "Classics")
        m1 = _m(client, name="Hamlet", type_="book")
        m2 = _m(client, name="Othello", type_="book")
        _m(client, name="Dune", type_="book")  # not associated
        client.post(f"{MEDIA_BASE}/{m1['id']}/topics/{t['id']}")
        client.post(f"{MEDIA_BASE}/{m2['id']}/topics/{t['id']}")
        items = _list(client, topic_id=t["id"])
        ids = [i["id"] for i in items]
        assert m1["id"] in ids
        assert m2["id"] in ids
        assert all(
            any(tp["id"] == t["id"] for tp in i["topics"]) for i in items
        )

    def test_topic_filter_excludes_unassociated(self, client: TestClient) -> None:
        """BDD-049 / AC-035: unassociated MediaItem excluded."""
        t = _t(client, "Classics")
        m_assoc = _m(client, name="Hamlet", type_="book")
        m_other = _m(client, name="Dune", type_="book")
        client.post(f"{MEDIA_BASE}/{m_assoc['id']}/topics/{t['id']}")
        items = _list(client, topic_id=t["id"])
        ids = [i["id"] for i in items]
        assert m_other["id"] not in ids

    def test_empty_topic_filter_returns_empty(self, client: TestClient) -> None:
        """BDD-050 / AC-035: topic with no associations → empty list."""
        t = _t(client, "Unassigned")
        _m(client, name="Dune", type_="book")
        items = _list(client, topic_id=t["id"])
        assert items == []


class TestCombinedFilters:
    """AC-036 / BDD-051: AND logic when multiple filters active."""

    def test_type_and_status_filter(self, client: TestClient) -> None:
        """BDD-051 / AC-036: type=book AND status=completed — only matching item."""
        _m(client, name="Book Done", type_="book", status="completed")
        _m(client, name="Book Planned", type_="book", status="planned")
        _m(client, name="Movie Done", type_="movie", status="completed")
        items = _list(client, type="book", status="completed")
        assert len(items) == 1
        assert items[0]["name"] == "Book Done"

    def test_no_match_combined_filters_empty(self, client: TestClient) -> None:
        """AC-036: no item matches all active filters → empty list."""
        _m(client, name="Book Planned", type_="book", status="planned")
        items = _list(client, type="book", status="completed")
        assert items == []
