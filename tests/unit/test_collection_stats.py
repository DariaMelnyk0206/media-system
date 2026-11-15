"""
TEST-016 — Collection Statistics (GET /api/stats)

Coverage:
  REQ-F-070..074
  AC-070..075
  BDD-071..075
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.repository import media_item_repo

STATS_URL = "/api/stats"
MEDIA_URL = "/api/media-items"
TOPIC_URL = "/api/topics"
STATUS_VALUES = ["planned", "in_progress", "postponed", "abandoned", "completed"]
TYPE_VALUES = ["book", "movie", "tv_series", "article", "podcast", "video", "other"]
LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "system.log"


def _create_media_item(
    client: TestClient,
    name: str,
    media_type: str = "book",
    status: str = "planned",
    rating: int | None = None,
) -> dict:
    payload = {"name": name, "type": media_type, "status": status}
    if rating is not None:
        payload["rating"] = rating
    response = client.post(MEDIA_URL, json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def _create_topic(client: TestClient, name: str) -> dict:
    response = client.post(TOPIC_URL, json={"name": name})
    assert response.status_code == 201, response.text
    return response.json()


def _associate(client: TestClient, item_id: str, topic_id: str) -> None:
    response = client.post(f"{MEDIA_URL}/{item_id}/topics/{topic_id}")
    assert response.status_code == 200, response.text


def _make_client(storage_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Create a client using the same store path to simulate a restart."""
    monkeypatch.setenv("PMLS_STORE_PATH", str(storage_path))
    return TestClient(app, raise_server_exceptions=True)


def _empty_status_counts() -> dict[str, int]:
    return dict.fromkeys(STATUS_VALUES, 0)


def _empty_type_counts() -> dict[str, int]:
    return dict.fromkeys(TYPE_VALUES, 0)


class TestCollectionStats:
    """Public contract for the read-only collection statistics endpoint."""

    def test_empty_collection_returns_zeroed_aggregates(
        self, client: TestClient
    ) -> None:
        """BDD-071 / AC-074: empty store returns complete zero-value schema."""
        response = client.get(STATS_URL)

        assert response.status_code == 200, response.text
        assert response.json() == {
            "total_media_items": 0,
            "total_topics": 0,
            "status_counts": _empty_status_counts(),
            "type_counts": _empty_type_counts(),
            "average_rating": None,
            "rated_count": 0,
            "topics_summary": [],
        }

    def test_totals_and_full_status_type_distributions(
        self, client: TestClient
    ) -> None:
        """REQ-F-070..071 / AC-070..071: every enum value is counted."""
        statuses = [
            "planned",
            "in_progress",
            "postponed",
            "abandoned",
            "completed",
            "planned",
            "completed",
        ]
        for index, (media_type, status) in enumerate(zip(TYPE_VALUES, statuses, strict=True)):
            _create_media_item(client, f"Item {index}", media_type, status)
        _create_topic(client, "One")
        _create_topic(client, "Two")

        response = client.get(STATS_URL)
        assert response.status_code == 200, response.text
        stats = response.json()
        assert stats["total_media_items"] == len(TYPE_VALUES)
        assert stats["total_topics"] == 2
        assert stats["type_counts"] == dict.fromkeys(TYPE_VALUES, 1)
        assert stats["status_counts"] == {
            "planned": 2,
            "in_progress": 1,
            "postponed": 1,
            "abandoned": 1,
            "completed": 2,
        }
        assert sum(stats["status_counts"].values()) == stats["total_media_items"]
        assert sum(stats["type_counts"].values()) == stats["total_media_items"]

    def test_average_rating_and_count_exclude_unrated_items(
        self, client: TestClient
    ) -> None:
        """BDD-072 / AC-072: only non-null ratings contribute to the mean."""
        _create_media_item(client, "Rated Eight", rating=8)
        _create_media_item(client, "Rated Seven", rating=7)
        _create_media_item(client, "Unrated")

        response = client.get(STATS_URL)
        assert response.status_code == 200, response.text
        stats = response.json()
        assert stats["average_rating"] == 7.5
        assert stats["rated_count"] == 2
        assert stats["total_media_items"] == 3

    def test_topics_summary_counts_many_to_many_and_sorts_deterministically(
        self, client: TestClient
    ) -> None:
        """BDD-073 / AC-073: each Topic count reflects distinct linked items."""
        first = _create_media_item(client, "First")
        second = _create_media_item(client, "Second")
        third = _create_media_item(client, "Third")
        topics = {
            name: _create_topic(client, name)
            for name in ["Science", "Space", "Alpha", "Beta", "Empty"]
        }
        for item, topic_name in [
            (first, "Science"),
            (first, "Space"),
            (second, "Science"),
            (second, "Alpha"),
            (third, "Beta"),
        ]:
            _associate(client, item["id"], topics[topic_name]["id"])

        response = client.get(STATS_URL)
        assert response.status_code == 200, response.text
        summary = response.json()["topics_summary"]
        assert [(entry["name"], entry["media_item_count"]) for entry in summary] == [
            ("Science", 2),
            ("Alpha", 1),
            ("Beta", 1),
            ("Space", 1),
            ("Empty", 0),
        ]
        assert all(set(entry) == {"id", "name", "media_item_count"} for entry in summary)

    def test_statistics_request_is_logged_without_user_authored_data(
        self, client: TestClient
    ) -> None:
        """BDD-074 / AC-075: log event identifies request without private text."""
        _create_media_item(client, "Private Item Marker")
        log_offset = LOG_PATH.stat().st_size if LOG_PATH.exists() else 0

        response = client.get(STATS_URL)

        assert response.status_code == 200, response.text
        new_log = LOG_PATH.read_bytes()[log_offset:].decode("utf-8")
        assert "stats.query" in new_log
        assert "status=200" in new_log
        assert "Private Item Marker" not in new_log

    def test_statistics_persist_across_application_restart(
        self,
        storage_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Statistics are derived from persisted records, not transient counters."""
        with _make_client(storage_path, monkeypatch) as first_client:
            _create_media_item(first_client, "Persistent", rating=9)
            _create_topic(first_client, "Persistent Topic")
            first_response = first_client.get(STATS_URL)
            assert first_response.status_code == 200, first_response.text
            expected = first_response.json()

        assert storage_path.exists()
        assert "media_items" in json.loads(storage_path.read_text(encoding="utf-8"))

        with _make_client(storage_path, monkeypatch) as restarted_client:
            restarted_response = restarted_client.get(STATS_URL)

        assert restarted_response.status_code == 200, restarted_response.text
        assert restarted_response.json() == expected

    def test_processing_failure_returns_error_response_and_is_logged(
        self,
        client: TestClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """BDD-075 / AC-075: processing failure maps to the standard HTTP 500."""
        log_offset = LOG_PATH.stat().st_size if LOG_PATH.exists() else 0

        def fail_listing() -> list:
            raise RuntimeError("simulated statistics failure")

        monkeypatch.setattr(media_item_repo, "list_all", fail_listing)
        response = client.get(STATS_URL)

        assert response.status_code == 500
        assert set(response.json()) == {"error", "field", "message"}
        new_log = LOG_PATH.read_bytes()[log_offset:].decode("utf-8")
        assert "stats.query" in new_log
        assert "status=500" in new_log
