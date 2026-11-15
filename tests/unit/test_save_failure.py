"""
tests/unit/test_save_failure.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TEST-015 — Save Failure Notification

SRS coverage:
  AC-050  user notified when auto-save fails (REQ-F-060)
  AC-051  change remains visible in session after save failure (REQ-F-061)
  AC-062  save failure notification present in response

BDD coverage: BDD-057, BDD-058, BDD-059 (persistence failure scenarios)

Mechanism:
  We inject a save failure by monkeypatching the filesystem write in the
  repository layer.  Since the repository module is not yet implemented
  (Phase 3), the patch target is the stdlib ``builtins.open`` for paths
  matching the store file, or a dedicated ``src.repository.storage.save``
  symbol (whichever the implementation exposes).

  The test must remain valid regardless of the exact save implementation;
  it patches ``builtins.open`` via the ``unittest.mock`` module to raise
  ``OSError`` when the store path is written.
"""

from __future__ import annotations

import builtins
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.sample_data import ERR_SAVE_FAILED

MEDIA_BASE = "/api/media-items"
TOPIC_BASE = "/api/topics"


def _raise_on_write(store_path: Path):
    """Context manager that makes any ``open(..., 'w')`` of store_path raise OSError."""
    real_open = builtins.open

    def patched_open(file, mode="r", *args, **kwargs):
        if str(file) == str(store_path) and "w" in str(mode):
            raise OSError("Simulated disk full")
        return real_open(file, mode, *args, **kwargs)

    return patch("builtins.open", side_effect=patched_open)


class TestSaveFailure:
    """TEST-015: auto-save failure returns 500 with save_failed error code
    while the in-session change remains visible."""

    def test_create_save_failure_returns_500(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-050 / BDD-057: when save fails on create → 500."""
        with _raise_on_write(storage_path):
            resp = client.post(MEDIA_BASE, json={"name": "Unsaved", "type": "book"})
        assert resp.status_code == 500, resp.text

    def test_create_save_failure_error_code(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-050: response body error.error == 'save_failed'."""
        with _raise_on_write(storage_path):
            resp = client.post(MEDIA_BASE, json={"name": "Unsaved", "type": "book"})
        assert resp.json()["error"] == ERR_SAVE_FAILED

    def test_create_save_failure_error_field_null(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """api-design-spec §3: save_failed error.field == null."""
        with _raise_on_write(storage_path):
            resp = client.post(MEDIA_BASE, json={"name": "Unsaved", "type": "book"})
        assert resp.json()["field"] is None

    def test_create_save_failure_message_present(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-062: error.message is non-empty string."""
        with _raise_on_write(storage_path):
            resp = client.post(MEDIA_BASE, json={"name": "Unsaved", "type": "book"})
        assert isinstance(resp.json()["message"], str)
        assert len(resp.json()["message"]) > 0

    def test_change_visible_in_session_after_save_failure(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-051 / BDD-058: item is in GET list even though save failed."""
        with _raise_on_write(storage_path):
            resp = client.post(MEDIA_BASE, json={"name": "Session Only", "type": "book"})
        # Even though save failed, check if item appears in the in-memory list
        # (REQ-F-061: change remains available for the current session)
        list_resp = client.get(MEDIA_BASE)
        assert list_resp.status_code == 200
        names = [i["name"] for i in list_resp.json()["data"]]
        assert "Session Only" in names

    def test_patch_save_failure_returns_500(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-050 / BDD-059: when save fails on PATCH → 500."""
        resp = client.post(MEDIA_BASE, json={"name": "Existing", "type": "book"})
        assert resp.status_code == 201
        item_id = resp.json()["id"]
        with _raise_on_write(storage_path):
            patch_resp = client.patch(
                f"{MEDIA_BASE}/{item_id}", json={"status": "completed"}
            )
        assert patch_resp.status_code == 500, patch_resp.text
        assert patch_resp.json()["error"] == ERR_SAVE_FAILED

    def test_delete_save_failure_returns_500(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-050: when save fails on DELETE → 500."""
        resp = client.post(MEDIA_BASE, json={"name": "ToDelete", "type": "book"})
        assert resp.status_code == 201
        item_id = resp.json()["id"]
        with _raise_on_write(storage_path):
            del_resp = client.delete(f"{MEDIA_BASE}/{item_id}")
        assert del_resp.status_code == 500, del_resp.text
        assert del_resp.json()["error"] == ERR_SAVE_FAILED

    def test_previous_data_not_corrupted_by_save_failure(
        self, client: TestClient, storage_path: Path
    ) -> None:
        """AC-050: previously persisted data intact after failed save."""
        # Create and successfully save item A
        resp_a = client.post(MEDIA_BASE, json={"name": "SafeItem", "type": "book"})
        assert resp_a.status_code == 201
        item_a_id = resp_a.json()["id"]

        # Attempt to create item B with save failure
        with _raise_on_write(storage_path):
            client.post(MEDIA_BASE, json={"name": "FailItem", "type": "book"})

        # Item A should still be retrievable
        resp_check = client.get(f"{MEDIA_BASE}/{item_a_id}")
        assert resp_check.status_code == 200, (
            "Previously persisted item should not be affected by a failed save"
        )
