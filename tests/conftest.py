"""
tests/conftest.py
~~~~~~~~~~~~~~~~~
Shared pytest fixtures for the Personal Media Library System test suite.

Phase 2 — Test Suite (PEP-001)
Ticket: TEST-001..015

Fixtures
--------
client
    A FastAPI TestClient backed by the application.
    Every test that uses this fixture gets a fresh, isolated JSON store
    at a temporary path — the production ``data/media_store.json`` is
    never touched during tests.

storage_path
    The resolved Path object pointing to the per-test JSON store.
    Useful for TEST-014 (autosave) and TEST-015 (save failure) which need
    to inspect or manipulate the file directly.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.main import app

# ---------------------------------------------------------------------------
# Storage isolation
# ---------------------------------------------------------------------------

# The environment variable read by the repository layer to determine where
# to persist data.  Defined here as a constant so tests and src code share
# the same name without hard-coding it in multiple places.
STORE_PATH_ENV = "PMLS_STORE_PATH"


@pytest.fixture()
def storage_path(tmp_path: Path) -> Path:
    """Return a fresh temporary file path for the JSON store.

    The file does not exist yet — the repository layer must create it on
    first save.  Using ``tmp_path`` (pytest's built-in per-test temp dir)
    guarantees isolation between tests and automatic cleanup after each run.
    """
    return tmp_path / "media_store.json"


@pytest.fixture()
def client(storage_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Return a TestClient wired to an isolated JSON store.

    The fixture:
    1. Sets ``PMLS_STORE_PATH`` to a unique temp path so the repository
       layer writes to a throwaway file, not ``data/media_store.json``.
    2. Yields a synchronous ``TestClient`` that exercises the full ASGI
       middleware stack (including the logging middleware in ``src/main.py``).
    3. Cleans up automatically when the test ends (monkeypatch is function-
       scoped by default).

    Usage::

        def test_something(client: TestClient) -> None:
            response = client.post("/api/media-items", json={...})
            assert response.status_code == 201
    """
    monkeypatch.setenv(STORE_PATH_ENV, str(storage_path))

    # Also patch the os.environ view that the repository may read at module
    # level *after* import (some implementations call os.getenv lazily).
    with TestClient(app, raise_server_exceptions=True) as tc:
        yield tc
