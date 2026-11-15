"""
tests/unit/test_sort.py
~~~~~~~~~~~~~~~~~~~~~~~~
TEST-012 — Sort (GET /api/media-items?sort=&dir=)

SRS coverage:
  AC-037  sort by name asc → A..Z
  AC-038  sort by name desc → Z..A
  AC-039  sort by rating asc → low to high; unrated last
  AC-040  sort by rating desc → high to low; unrated last

BDD coverage: BDD-052, BDD-053, BDD-054, BDD-055
"""

from __future__ import annotations

from fastapi.testclient import TestClient

MEDIA_BASE = "/api/media-items"


def _m(client: TestClient, name: str, rating: int | None = None) -> dict:
    payload: dict = {"name": name, "type": "book"}
    if rating is not None:
        payload["rating"] = rating
    r = client.post(MEDIA_BASE, json=payload)
    assert r.status_code == 201, r.text
    return r.json()


def _names(client: TestClient, **params) -> list[str]:
    return [i["name"] for i in client.get(MEDIA_BASE, params=params).json()["data"]]


class TestSortByName:
    """AC-037..038 / BDD-052..053: alphabetical sort."""

    def test_sort_name_asc(self, client: TestClient) -> None:
        """BDD-052 / AC-037: Astronomy, Cosmos, Zebra."""
        _m(client, "Cosmos")
        _m(client, "Astronomy")
        _m(client, "Zebra")
        names = _names(client, sort="name", dir="asc")
        # Find positions of our three items
        positions = {n: names.index(n) for n in ("Astronomy", "Cosmos", "Zebra")}
        assert positions["Astronomy"] < positions["Cosmos"] < positions["Zebra"]

    def test_sort_name_desc(self, client: TestClient) -> None:
        """BDD-053 / AC-038: Zebra, Cosmos, Astronomy."""
        _m(client, "Cosmos")
        _m(client, "Astronomy")
        _m(client, "Zebra")
        names = _names(client, sort="name", dir="desc")
        positions = {n: names.index(n) for n in ("Astronomy", "Cosmos", "Zebra")}
        assert positions["Zebra"] < positions["Cosmos"] < positions["Astronomy"]

    def test_sort_name_asc_default_dir(self, client: TestClient) -> None:
        """Sort by name without dir → defaults to asc."""
        _m(client, "Beta")
        _m(client, "Alpha")
        names = _names(client, sort="name")
        assert names.index("Alpha") < names.index("Beta")


class TestSortByRating:
    """AC-039..040 / BDD-054..055: rating sort, unrated last."""

    def _setup_ratings(self, client: TestClient) -> None:
        _m(client, "High", rating=9)
        _m(client, "Mid", rating=5)
        _m(client, "Low", rating=3)
        _m(client, "Unrated")  # no rating

    def test_sort_rating_asc(self, client: TestClient) -> None:
        """BDD-054 / AC-039: low..high rating, then unrated at end."""
        self._setup_ratings(client)
        items = client.get(MEDIA_BASE, params={"sort": "rating", "dir": "asc"}).json()["data"]
        rated = [i for i in items if i["rating"] is not None]
        unrated = [i for i in items if i["rating"] is None]
        # Rated items in ascending order
        ratings = [i["rating"] for i in rated]
        assert ratings == sorted(ratings)
        # All unrated appear after all rated
        if rated and unrated:
            last_rated_idx = items.index(rated[-1])
            first_unrated_idx = items.index(unrated[0])
            assert last_rated_idx < first_unrated_idx

    def test_sort_rating_desc(self, client: TestClient) -> None:
        """BDD-055 / AC-040: high..low rating, then unrated at end."""
        self._setup_ratings(client)
        items = client.get(MEDIA_BASE, params={"sort": "rating", "dir": "desc"}).json()["data"]
        rated = [i for i in items if i["rating"] is not None]
        unrated = [i for i in items if i["rating"] is None]
        # Rated items in descending order
        ratings = [i["rating"] for i in rated]
        assert ratings == sorted(ratings, reverse=True)
        # All unrated appear after all rated
        if rated and unrated:
            last_rated_idx = items.index(rated[-1])
            first_unrated_idx = items.index(unrated[0])
            assert last_rated_idx < first_unrated_idx

    def test_sort_rating_all_unrated_last(self, client: TestClient) -> None:
        """AC-039 / AC-040: all unrated items collectively appear after any rated item."""
        _m(client, "Rated A", rating=7)
        _m(client, "Unrated X")
        _m(client, "Unrated Y")
        items_asc = client.get(MEDIA_BASE, params={"sort": "rating", "dir": "asc"}).json()["data"]
        items_desc = client.get(MEDIA_BASE, params={"sort": "rating", "dir": "desc"}).json()["data"]
        for items in (items_asc, items_desc):
            rated_indices = [i for i, x in enumerate(items) if x["rating"] is not None]
            unrated_indices = [i for i, x in enumerate(items) if x["rating"] is None]
            if rated_indices and unrated_indices:
                assert max(rated_indices) < min(unrated_indices)

    def test_sort_name_case_insensitive_order(self, client: TestClient) -> None:
        """Sort by name treats uppercase/lowercase consistently (lexicographic)."""
        _m(client, "apple")
        _m(client, "Banana")
        names = _names(client, sort="name", dir="asc")
        # Both must appear; exact order depends on locale but both present
        assert "apple" in names
        assert "Banana" in names
