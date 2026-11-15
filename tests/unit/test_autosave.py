"""
tests/unit/test_autosave.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-014 — Auto-save та Persistence

SRS coverage:
  AC-005   created item persists to file (REQ-F-008, REQ-NF-005)
  AC-049   any mutating operation auto-saves
  AC-061   no explicit Save action needed
  AC-063   on startup, library reflects last saved state

BDD coverage: BDD-003, BDD-011, BDD-034
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.main import app

MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"
STORE_PATH_ENV = "PMLS_STORE_PATH"


def _make_client(storage_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Create a TestClient pinned to the given storage path."""
    monkeypatch.setenv(STORE_PATH_ENV, str(storage_path))
    return TestClient(app, raise_server_exceptions=True)


class TestAutoSave:
    """Persistence: data written to JSON file and reloaded on new client."""

    def test_create_writes_to_json(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-005 / BDD-003: after POST, storage file exists."""
        with _make_client(storage_path, monkeypatch) as tc:
            tc.post(MEDIA_BASE, json={"name": "Foundation", "type": "book"})
        assert storage_path.exists(), "Storage file should be written after create"

    def test_created_item_in_json(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-005: created item's data present in the JSON file."""
        with _make_client(storage_path, monkeypatch) as tc:
            resp = tc.post(MEDIA_BASE, json={"name": "Foundation", "type": "book"})
            item_id = resp.json()["id"]
        data = json.loads(storage_path.read_text(encoding="utf-8"))
        # The JSON structure is implementation-defined; we just check the id appears
        assert item_id in json.dumps(data), "Created item id not found in store file"

    def test_new_client_loads_persisted_item(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-063 / BDD-003: second client instance sees item saved by first."""
        # Session 1 — create
        with _make_client(storage_path, monkeypatch) as tc1:
            resp = tc1.post(MEDIA_BASE, json={"name": "Foundation", "type": "book"})
            item_id = resp.json()["id"]

        # Session 2 — new TestClient same file = simulates app restart
        with _make_client(storage_path, monkeypatch) as tc2:
            resp2 = tc2.get(f"{MEDIA_BASE}/{item_id}")
        assert resp2.status_code == 200, "Item should survive simulated restart"
        assert resp2.json()["name"] == "Foundation"

    def test_update_persists(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-049 / BDD-011: PATCH auto-saved; second session sees updated value."""
        with _make_client(storage_path, monkeypatch) as tc1:
            resp = tc1.post(MEDIA_BASE, json={"name": "Sapiens", "type": "book"})
            item_id = resp.json()["id"]
            tc1.patch(f"{MEDIA_BASE}/{item_id}", json={"status": "completed"})

        with _make_client(storage_path, monkeypatch) as tc2:
            resp2 = tc2.get(f"{MEDIA_BASE}/{item_id}")
        assert resp2.json()["status"] == "completed"

    def test_delete_persists(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-049: DELETE auto-saved; second session cannot find deleted item."""
        with _make_client(storage_path, monkeypatch) as tc1:
            resp = tc1.post(MEDIA_BASE, json={"name": "Deleted", "type": "book"})
            item_id = resp.json()["id"]
            tc1.delete(f"{MEDIA_BASE}/{item_id}")

        with _make_client(storage_path, monkeypatch) as tc2:
            resp2 = tc2.get(f"{MEDIA_BASE}/{item_id}")
        assert resp2.status_code == 404

    def test_topic_creation_persists(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-013 / BDD-018: Topic creation also auto-saved."""
        with _make_client(storage_path, monkeypatch) as tc1:
            resp = tc1.post(TOPIC_BASE, json={"name": "Philosophy"})
            topic_id = resp.json()["id"]

        with _make_client(storage_path, monkeypatch) as tc2:
            resp2 = tc2.get(f"{TOPIC_BASE}/{topic_id}")
        assert resp2.status_code == 200
        assert resp2.json()["name"] == "Philosophy"

    def test_association_persists(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-020 / BDD-034: association change survives restart."""
        with _make_client(storage_path, monkeypatch) as tc1:
            m = tc1.post(MEDIA_BASE, json={"name": "Origin", "type": "book"}).json()
            t = tc1.post(TOPIC_BASE, json={"name": "Science"}).json()
            tc1.post(f"{MEDIA_BASE}/{m['id']}/topics/{t['id']}")

        with _make_client(storage_path, monkeypatch) as tc2:
            body = tc2.get(f"{MEDIA_BASE}/{m['id']}").json()
        assert any(tp["id"] == t["id"] for tp in body["topics"])

    def test_multiple_creates_all_persist(
        self, storage_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """AC-049: multiple creates in one session, all visible after restart."""
        ids = []
        with _make_client(storage_path, monkeypatch) as tc1:
            for i in range(3):
                r = tc1.post(MEDIA_BASE, json={"name": f"Item {i}", "type": "book"})
                ids.append(r.json()["id"])

        with _make_client(storage_path, monkeypatch) as tc2:
            for item_id in ids:
                assert tc2.get(f"{MEDIA_BASE}/{item_id}").status_code == 200
