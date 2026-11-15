"""HTTP route for read-only collection statistics."""

from __future__ import annotations

from fastapi import APIRouter

from src.errors.error_codes import ErrorResponse
from src.logging.logger import get_logger
from src.models.collection_stats import CollectionStatsResponse
from src.services import collection_stats_service

log = get_logger(__name__)

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get(
    "",
    response_model=CollectionStatsResponse,
    status_code=200,
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Statistics could not be calculated.",
        }
    },
)
def get_collection_stats() -> CollectionStatsResponse:
    """Return read-only statistics for the current local collection."""
    return collection_stats_service.get_collection_stats()
