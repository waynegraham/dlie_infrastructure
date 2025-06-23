"""
Search endpoint for Solr-backed queries, now with keyword, semantic, and vector search.
"""
from fastapi import APIRouter, Query
from typing import List, Optional

from api.schemas import SearchResponse, SemanticSearchRequest, VectorSearchRequest
from api.solr_client import (
    search_resources,
    semantic_search_resources,
    vector_search_resources,
)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=SearchResponse)
def keyword_search(
    query: str = Query("", alias="query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    resource_type: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    keywords: Optional[List[str]] = Query(None),
):
    """
    Classic keyword and faceted search via Solr `/select`.
    If query is empty, returns all records.
    """
    # Facet on resource_type (not reserved 'type'), provider, and keywords
    facets = ["resource_type", "provider", "keywords"]
    qstr = "*:*" if not query else f"title:*{query}* OR abstract:*{query}*"
    filters = {}
    if resource_type:
        filters['resource_type'] = resource_type
    if provider:
        filters['provider'] = provider
    if keywords:
        filters['keywords'] = keywords

    return search_resources(
        q=qstr,
        page=page,
        page_size=page_size,
        facet_fields=facets,
        filters=filters,
    )


@router.post("/semantic", response_model=SearchResponse)
def semantic_search(req: SemanticSearchRequest):
    """
    On-the-fly semantic search using Solr `knn_text_to_vector`.
    """
    return semantic_search_resources(
        query=req.query,
        top_k=req.top_k,
        filters=req.filters,
        page=req.page,
        page_size=req.page_size,
    )


@router.post("/vector", response_model=SearchResponse)
def vector_search(req: VectorSearchRequest):
    """
    Precomputed-vector search hitting Solr `/knn` with `emb_vector`.
    """
    print("DEBUG request JSON:", req)
    return vector_search_resources(
        vector=req.vector,
        top_k=req.top_k,
        filters=req.filters,
        page=req.page,
        page_size=req.page_size,
    )
