"""
tests/unit/test_search.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-010 — Search (GET /api/search)

SRS coverage:
  AC-023  MediaItems matched by name substring (case-insensitive)
  AC-024  Topics matched by name, identifiable as 'topic'
  AC-025  Topic result openable (navigable)
  AC-026  mixed results with kind discriminator
  AC-027  empty query → empty results
  AC-028  notes NOT searched

BDD coverage: BDD-037, BDD-038, BDD-039, BDD-040, BDD-041, BDD-042
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.fixtures.sample_data import (
    MEDIA_OCEAN_DEEP,
    MEDIA_SPACE_ODYSSEY,
    MEDIA_SPACE_TRAVEL,
    MEDIA_WITH_NOTES_COSMOS,
)

SEARCH_BASE = "/api/search"
MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _media(client: TestClient, payload: dict) -> dict:
    r = client.post(MEDIA_BASE, json=payload)
    assert r.status_code == 201, r.text
    return r.json()


def _topic(client: TestClient, name: str) -> dict:
    r = client.post(TOPIC_BASE, json={"name": name})
    assert r.status_code == 201, r.text
    return r.json()


class TestSearch:
    """GET /api/search?q=<query>"""

    # --- Response shape ---

    def test_search_returns_200(self, client: TestClient) -> None:
        """GET /api/search?q=anything → 200."""
        resp = client.get(SEARCH_BASE, params={"q": "dune"})
        assert resp.status_code == 200, resp.text

    def test_search_response_has_data_list(self, client: TestClient) -> None:
        """Response body has 'data' array."""
        resp = client.get(SEARCH_BASE, params={"q": "x"})
        body = resp.json()
        assert "data" in body
        assert isinstance(body["data"], list)

    def test_search_result_has_kind_field(self, client: TestClient) -> None:
        """AC-026 / IR-024: each result item has a 'kind' discriminator."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        resp = client.get(SEARCH_BASE, params={"q": "Space"})
        for item in resp.json()["data"]:
            assert "kind" in item, "Result item missing 'kind' field"

    # --- MediaItem search (AC-023) ---

    def test_search_finds_media_by_name_substring(self, client: TestClient) -> None:
        """BDD-037 / AC-023: 'space' matches 'Space Odyssey' and 'space travel'."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        _media(client, MEDIA_SPACE_TRAVEL)
        _media(client, MEDIA_OCEAN_DEEP)
        resp = client.get(SEARCH_BASE, params={"q": "space"})
        names = [r["name"] for r in resp.json()["data"]]
        assert "Space Odyssey" in names
        assert "space travel guide" in names
        assert "Ocean Deep" not in names

    def test_search_case_insensitive(self, client: TestClient) -> None:
        """AC-023: search is case-insensitive."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        resp = client.get(SEARCH_BASE, params={"q": "SPACE"})
        names = [r["name"] for r in resp.json()["data"]]
        assert "Space Odyssey" in names

    def test_search_media_kind_is_media_item(self, client: TestClient) -> None:
        """AC-026: MediaItem results have kind == 'media_item'."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        resp = client.get(SEARCH_BASE, params={"q": "Space"})
        media_results = [r for r in resp.json()["data"] if r["name"] == "Space Odyssey"]
        assert len(media_results) == 1
        assert media_results[0]["kind"] == "media_item"

    # --- Topic search (AC-024) ---

    def test_search_finds_topic_by_name(self, client: TestClient) -> None:
        """BDD-038 / AC-024: 'sci' matches topic 'Science Fiction'."""
        _topic(client, "Science Fiction")
        _topic(client, "History")
        resp = client.get(SEARCH_BASE, params={"q": "sci"})
        names = [r["name"] for r in resp.json()["data"]]
        assert "Science Fiction" in names
        assert "History" not in names

    def test_search_topic_kind_is_topic(self, client: TestClient) -> None:
        """AC-024: Topic results have kind == 'topic'."""
        _topic(client, "Science Fiction")
        resp = client.get(SEARCH_BASE, params={"q": "Science"})
        topic_results = [
            r for r in resp.json()["data"] if r["name"] == "Science Fiction"
        ]
        assert len(topic_results) == 1
        assert topic_results[0]["kind"] == "topic"

    # --- Mixed results (AC-026) ---

    def test_search_returns_both_media_and_topic(self, client: TestClient) -> None:
        """BDD-039 / AC-026: same query matches both MediaItem and Topic."""
        _media(client, {"name": "Science", "type": "book"})
        _topic(client, "Science")
        resp = client.get(SEARCH_BASE, params={"q": "science"})
        kinds = {r["kind"] for r in resp.json()["data"]}
        assert "media_item" in kinds
        assert "topic" in kinds

    # --- Empty query (AC-027) ---

    def test_empty_query_returns_empty_data(self, client: TestClient) -> None:
        """BDD-041 / AC-027: empty q → empty data list."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        resp = client.get(SEARCH_BASE, params={"q": ""})
        assert resp.status_code == 200, resp.text
        assert resp.json()["data"] == []

    # --- Notes not searchable (AC-028) ---

    def test_notes_not_included_in_search(self, client: TestClient) -> None:
        """BDD-042 / AC-028: notes content does not cause item to appear in results."""
        _media(client, MEDIA_WITH_NOTES_COSMOS)  # name has no "cosmos"
        resp = client.get(SEARCH_BASE, params={"q": "cosmos"})
        names = [r["name"] for r in resp.json()["data"]]
        assert "Arrival Extra" not in names

    # --- No matches ---

    def test_no_match_returns_empty_list(self, client: TestClient) -> None:
        """Query with no matches → data == []."""
        _media(client, MEDIA_SPACE_ODYSSEY)
        resp = client.get(SEARCH_BASE, params={"q": "xyzqrst"})
        assert resp.json()["data"] == []
