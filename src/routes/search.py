"""
src/routes/search.py
~~~~~~~~~~~~~~~~~~~~~
Unified search endpoint.

Endpoint:
  GET /search?q=<query>    search  (FEAT-008, REQ-F-038..043)

Response: {"data": [SearchResultItem, ...]}

Each SearchResultItem carries a ``kind`` discriminator:
  "media_item" -- matched MediaItem (name, type, status, rating)
  "topic"      -- matched Topic (name only; type/status/rating are null)

Empty or whitespace-only ``q`` returns {"data": []} immediately
without searching (AC-027, REQ-F-042).
"""

from __future__ import annotations

from fastapi import APIRouter

from src.errors.error_codes import ErrorResponse
from src.logging.logger import get_logger
from src.models.topic import SearchResponse, SearchResultItem
from src.services import search_service

log = get_logger(__name__)

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "",
    response_model=SearchResponse,
    status_code=200,
    responses={400: {"model": ErrorResponse, "description": "Invalid query parameter"}},
)
def search(q: str = "") -> SearchResponse:
    """Unified search across MediaItems and Topics (FEAT-008, REQ-F-038..043).

    Args:
        q: Substring query -- case-insensitive match on entity names.
           Empty string returns empty list (AC-027).

    Returns:
        SearchResponse with data list of SearchResultItem.
    """
    results: list[SearchResultItem] = search_service.search(q)
    return SearchResponse(data=results)
