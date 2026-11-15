"""
tests/fixtures/sample_data.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Canonical test data for the Personal Media Library System test suite.

All values are aligned with the domain contracts defined in:
  - spec/srs.md  (VR-001..011, CON-001..002)
  - docs/openapi.yaml  (CreateMediaItemRequest, CreateTopicRequest schemas)

Phase 2 — Test Suite (PEP-001)
"""

from __future__ import annotations

# =============================================================================
# Valid MediaItem payloads
# =============================================================================

# Minimal valid payload — required fields only (BDD-001)
MEDIA_MINIMAL: dict = {
    "name": "Dune",
    "type": "book",
}

# Full valid payload — all optional fields provided (BDD-002)
MEDIA_FULL: dict = {
    "name": "Arrival",
    "type": "movie",
    "status": "completed",
    "notes": "Excellent film about language and time.",
    "rating": 9,
    "topic_ids": [],
}

# Used for PATCH tests — partial update
MEDIA_PATCH_STATUS: dict = {"status": "completed"}
MEDIA_PATCH_RATING: dict = {"rating": 7}
MEDIA_PATCH_NOTES: dict = {"notes": "Updated notes."}
MEDIA_PATCH_CLEAR_RATING: dict = {"rating": None}
MEDIA_PATCH_CLEAR_NOTES: dict = {"notes": None}

# A set of MediaItems with varied types, statuses, ratings for filter/sort tests
MEDIA_BOOK_PLANNED: dict = {"name": "Foundation", "type": "book", "status": "planned"}
MEDIA_BOOK_COMPLETED: dict = {
    "name": "Sapiens",
    "type": "book",
    "status": "completed",
    "rating": 8,
}
MEDIA_MOVIE_COMPLETED: dict = {
    "name": "Interstellar",
    "type": "movie",
    "status": "completed",
    "rating": 9,
}
MEDIA_MOVIE_IN_PROGRESS: dict = {
    "name": "Gravity",
    "type": "movie",
    "status": "in_progress",
    "rating": 7,
}
MEDIA_ARTICLE_PLANNED: dict = {
    "name": "Space Odyssey Article",
    "type": "article",
    "status": "planned",
}
MEDIA_PODCAST_POSTPONED: dict = {
    "name": "History Podcast",
    "type": "podcast",
    "status": "postponed",
    "rating": 5,
}
MEDIA_NO_RATING: dict = {
    "name": "Unrated Book",
    "type": "book",
    "status": "planned",
}

# MediaItems for search tests
MEDIA_SPACE_ODYSSEY: dict = {"name": "Space Odyssey", "type": "movie"}
MEDIA_SPACE_TRAVEL: dict = {"name": "space travel guide", "type": "book"}
MEDIA_OCEAN_DEEP: dict = {"name": "Ocean Deep", "type": "book"}

# MediaItem with notes that contain a word NOT in its name (BDD-042)
MEDIA_WITH_NOTES_COSMOS: dict = {
    "name": "Arrival Extra",
    "type": "movie",
    "notes": "contains the word cosmos",
}

# MediaItems for sort tests (BDD-052, BDD-053, BDD-054, BDD-055)
MEDIA_SORT_COSMOS: dict = {"name": "Cosmos", "type": "book", "rating": 6}
MEDIA_SORT_ASTRONOMY: dict = {"name": "Astronomy", "type": "book", "rating": 9}
MEDIA_SORT_ZEBRA: dict = {"name": "Zebra", "type": "book", "rating": 3}
MEDIA_SORT_UNRATED: dict = {"name": "Unrated Alpha", "type": "book"}

# MediaItems for rating filter tests
MEDIA_RATING_5: dict = {"name": "Rating Five", "type": "book", "rating": 5}
MEDIA_RATING_7: dict = {"name": "Rating Seven", "type": "book", "rating": 7}
MEDIA_RATING_9: dict = {"name": "Rating Nine", "type": "book", "rating": 9}

# =============================================================================
# Valid Topic payloads
# =============================================================================

TOPIC_SCI_FI: dict = {"name": "Science Fiction"}
TOPIC_HISTORY: dict = {"name": "History"}
TOPIC_SPACE: dict = {"name": "Space"}
TOPIC_CLASSICS: dict = {"name": "Classics"}
TOPIC_UNASSIGNED: dict = {"name": "Unassigned"}

# =============================================================================
# Invalid / boundary-violating payloads  (VR-001..011)
# =============================================================================

# VR-001: empty name → error.error == "name_required", error.field == "name"
MEDIA_EMPTY_NAME: dict = {"name": "", "type": "book"}

# VR-001: whitespace-only name (BDD-005)
MEDIA_WHITESPACE_NAME: dict = {"name": "   ", "type": "podcast"}

# VR-007: rating above max (BDD-007)
MEDIA_RATING_TOO_HIGH: dict = {"name": "Neuromancer", "type": "book", "rating": 11}

# VR-007: rating of zero (BDD-008)
MEDIA_RATING_ZERO: dict = {"name": "Ghost in the Shell", "type": "movie", "rating": 0}

# VR-007: rating below min — negative
MEDIA_RATING_NEGATIVE: dict = {"name": "Bad Rating", "type": "book", "rating": -1}

# VR-008: invalid type
MEDIA_INVALID_TYPE: dict = {"name": "Unknown Type", "type": "comic"}

# VR-009: invalid status
MEDIA_INVALID_STATUS: dict = {
    "name": "Bad Status",
    "type": "book",
    "status": "watching",
}

# VR-003: topic with empty name
TOPIC_EMPTY_NAME: dict = {"name": ""}

# VR-003: topic with whitespace-only name
TOPIC_WHITESPACE_NAME: dict = {"name": "   "}

# VR-002 / name trimming: MediaItem name with leading/trailing spaces (BDD-006)
MEDIA_PADDED_NAME: dict = {"name": "  Cosmos  ", "type": "video"}
MEDIA_PADDED_NAME_EXPECTED: str = "Cosmos"

# VR-004 / name trimming: Topic name with spaces (BDD-022)
TOPIC_PADDED_NAME: dict = {"name": "  History  "}
TOPIC_PADDED_NAME_EXPECTED: str = "History"

# =============================================================================
# Error response field constants (api-design-spec §3)
# =============================================================================

# These string constants are the machine-readable error codes from openapi.yaml.
# Tests assert against these values so a typo in production code is caught.
ERR_NAME_REQUIRED = "name_required"
ERR_RATING_OUT_OF_RANGE = "rating_out_of_range"
ERR_INVALID_TYPE = "invalid_type"
ERR_INVALID_STATUS = "invalid_status"
ERR_INVALID_RATING_RANGE = "invalid_rating_range"
ERR_INVALID_RATING_BOUND = "invalid_rating_bound"
ERR_NAME_TAKEN = "name_taken"
ERR_NOT_FOUND = "not_found"
ERR_SAVE_FAILED = "save_failed"

# Field names referenced in error responses
FIELD_NAME = "name"
FIELD_RATING = "rating"
FIELD_TYPE = "type"
FIELD_STATUS = "status"
FIELD_RATING_MIN = "rating_min"
