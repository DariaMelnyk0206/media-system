"""
src/repository/storage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~
JSON file persistence layer.

Responsibilities:
  - Determine store path from env var PMLS_STORE_PATH (default: data/media_store.json)
  - Load state from disk on application startup
  - Save state to disk after every mutating operation (REQ-F-059)
  - Raise SaveFailedError on IOError/OSError so the caller returns 500 (REQ-F-060)
  - Keep in-memory state intact even when save fails (REQ-F-061)

Store format (JSON):
  {
    "media_items": { "<uuid>": { ...MediaItem fields, "topic_ids": [...] } },
    "topics":      { "<uuid>": { "id": "...", "name": "..." } }
  }

Associations are stored as "topic_ids" list inside each media_item entry.
Topic objects are stored without a media_items list — the list is derived
at read time by inverting the media_item → topic_ids mapping.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from src.errors.handlers import SaveFailedError
from src.logging.logger import get_logger

log = get_logger(__name__)

# ---------------------------------------------------------------------------
# In-memory store — module-level singletons
# ---------------------------------------------------------------------------

# { uuid_str: dict }  — raw dicts, identical to what we persist in JSON
_media_items: dict[str, dict] = {}
_topics: dict[str, dict] = {}


def get_media_items() -> dict[str, dict]:
    return _media_items


def get_topics() -> dict[str, dict]:
    return _topics


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

_DEFAULT_PATH = Path("data") / "media_store.json"


def _store_path() -> Path:
    env = os.environ.get("PMLS_STORE_PATH")
    return Path(env) if env else _DEFAULT_PATH


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------


def load() -> None:
    """Load persisted data from disk into the in-memory store.

    Called once at application startup (lifespan).
    If the file does not exist, the store starts empty — no error.
    If the file is malformed JSON, it is logged and the store starts empty.
    """
    global _media_items, _topics
    path = _store_path()

    if not path.exists():
        log.info("store.load  path=%s  status=not_found  starting_empty", path)
        _media_items = {}
        _topics = {}
        return

    try:
        raw = path.read_text(encoding="utf-8")
        data: dict[str, Any] = json.loads(raw)
        _media_items = data.get("media_items", {})
        _topics = data.get("topics", {})
        log.info(
            "store.load  path=%s  media_items=%d  topics=%d",
            path,
            len(_media_items),
            len(_topics),
        )
    except (json.JSONDecodeError, OSError) as exc:
        log.error("store.load  path=%s  error=%s  starting_empty", path, exc)
        _media_items = {}
        _topics = {}


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------


def save() -> None:
    """Persist current in-memory state to the JSON store file.

    Uses an explicit ``open()`` call (not ``Path.write_text``) so that
    test code can inject failures via ``patch("builtins.open")``.

    Raises SaveFailedError (HTTP 500) if the write fails (REQ-F-060).
    In-memory state is NOT rolled back — the change remains available
    for the current session (REQ-F-061).
    """
    path = _store_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            {"media_items": _media_items, "topics": _topics},
            ensure_ascii=False,
            indent=2,
        )
        # Explicit open() so builtins.open patches work in tests (TEST-015).
        with open(str(path), "w", encoding="utf-8") as fh:
            fh.write(payload)
        log.debug(
            "store.save  path=%s  media_items=%d  topics=%d",
            path,
            len(_media_items),
            len(_topics),
        )
    except OSError as exc:
        log.error("store.save  FAILED  path=%s  error=%s", path, exc)
        raise SaveFailedError() from exc
