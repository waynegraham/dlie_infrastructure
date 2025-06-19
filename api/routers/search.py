"""
Search endpoint for Solr-backed queries.
"""
from fastapi import APIRouter, Query

from api.schemas import SearchResponse
from api.solr_client import search_resources

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search(
    query: str = Query("", alias="query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    facets = ["type", "provider", "keywords"]
    return search_resources(
        q=f"title:*{query}* OR abstract:*{query}*",
        page=page,
        page_size=page_size,
        facet_fields=facets,
    )