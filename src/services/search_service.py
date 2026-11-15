"""
src/services/search_service.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unified full-text search across MediaItems and Topics.

Covers FEAT-008 (unified search, REQ-F-038..043).

Search rules:
  - Substring, case-insensitive match on the entity **name** only.
  - Notes are NOT searched (CON-006, REQ-F-043, AC-028).
  - Empty or absent query → returns empty list (AC-027, REQ-F-042).
  - Both MediaItems and Topics are searched; results carry a ``kind``
    discriminator: "media_item" or "topic" (IR-024, SearchResultItem schema).

Logging events:
  search.query  — fired on every non-empty search call
"""

from __future__ import annotations

from src.logging.logger import get_logger
from src.models.topic import SearchResultItem
from src.repository import media_item_repo, topic_repo

log = get_logger(__name__)


def search(q: str) -> list[SearchResultItem]:
    """Execute a unified search across MediaItems and Topics.

    Args:
        q: Raw query string from the HTTP request.
           Empty or whitespace-only → returns [].

    Returns:
        List of :class:`SearchResultItem` ordered as:
        all matching MediaItems first (insertion order), then Topics.
    """
    q_stripped = q.strip() if q else ""

    # Empty / whitespace query → no results (AC-027)
    if not q_stripped:
        log.debug("search.query  q=%r  empty → returning []", q)
        return []

    q_lower = q_stripped.lower()
    log.info("search.query  q=%r", q_stripped)

    results: list[SearchResultItem] = []

    # --- Search MediaItems by name (REQ-F-040, AC-023) ---
    for item in media_item_repo.list_all():
        if q_lower in item.name.lower():
            results.append(
                SearchResultItem(
                    kind="media_item",
                    id=item.id,
                    name=item.name,
                    type=item.type.value,
                    status=item.status.value,
                    rating=item.rating,
                )
            )

    # --- Search Topics by name (REQ-F-041, AC-024) ---
    for topic in topic_repo.list_all():
        if q_lower in topic.name.lower():
            results.append(
                SearchResultItem(
                    kind="topic",
                    id=topic.id,
                    name=topic.name,
                    type=None,
                    status=None,
                    rating=None,
                )
            )

    log.info("search.results  q=%r  count=%d", q_stripped, len(results))
    return results
