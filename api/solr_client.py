import requests
import pysolr
from typing import Any, Dict, List, Optional, Union
from api.config import settings

# Pysolr client for basic indexing operations
_solr = pysolr.Solr(str(settings.solr_url), always_commit=True, timeout=10)

# Base URL to call Solr HTTP APIs (assumes settings.solr_url points to core endpoint)
SOLR_BASE = str(settings.solr_url)


def index_resources(docs: list[dict]):
    """
    Batch‐index a list of Solr docs.
    """
    _solr.add(docs)


def delete_resource(resource_id: int):
    """
    Delete a resource by its ID from Solr.
    """
    _solr.delete(id=str(resource_id))


def _build_fq(filters: Optional[Dict[str, Union[str, List[str]]]] = None) -> List[str]:
    """
    Turn a dict of filters into Solr fq parameters, skipping invalid types.
    """
    fq: List[str] = []
    if not filters:
        return fq
    for field, val in filters.items():
        # Only support string or list of strings
        if isinstance(val, str):
            fq.append(f"{field}:{val}")
        elif isinstance(val, list) and all(isinstance(v, str) for v in val):
            vals = " OR ".join(val)
            fq.append(f"{field}:(" + vals + ")")
        else:
            # skip unsupported filter types
            continue
    return fq
    for field, val in filters.items():
        if isinstance(val, list):
            vals = " OR ".join(val)
            fq.append(f"{field}:(" + vals + ")")
        else:
            fq.append(f"{field}:{val}")
    return fq


def _flatten_string_field(value: Any) -> Optional[str]:
    """Helper to flatten list-of-string or return string, or None."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


def search_resources(
    q: str,
    page: int = 1,
    page_size: int = 10,
    facet_fields: List[str] = None,
    facet_limit: int = 10,
    filters: Optional[Dict[str, Union[str, List[str]]]] = None,
) -> Dict[str, Any]:
    """
    Classic keyword/faceted search via Solr `/select`.
    """
    params: Dict[str, Any] = {
        "q": q or "*:*",
        "start": (page - 1) * page_size,
        "rows": page_size,
        "wt": "json",
    }
    if facet_fields:
        params.update({
            "facet": "true",
            "facet.field": facet_fields,
            "facet.limit": facet_limit,
        })

    # add filter queries
    for fq in _build_fq(filters):
        params.setdefault("fq", []).append(fq)

    resp = requests.get(f"{SOLR_BASE}/select", params=params)
    resp.raise_for_status()
    resp_json = resp.json()
    results = resp_json.get("response", {})

    items = []
    for doc in results.get("docs", []):
        title = _flatten_string_field(doc.get("title"))
        date = _flatten_string_field(doc.get("date"))
        items.append({
            "id": doc.get("id"),
            "title": title,
            "authors": doc.get("authors", []),
            "date": date,
        })

    # parse facets
    facets: Dict[str, List[Dict[str, Union[str, int]]]] = {}
    if facet_fields:
        facet_counts = resp_json.get("facet_counts", {}).get("facet_fields", {})
        for field in facet_fields:
            counts = facet_counts.get(field, [])
            facets[field] = [
                {"label": counts[i], "value": counts[i], "count": counts[i+1]}
                for i in range(0, len(counts), 2)
            ]

    return {
        "items": items,
        "total": results.get("numFound", 0),
        "page_size": page_size,
        "facets": facets,
    }


def semantic_search_resources(
    query: str,
    top_k: int = 10,
    filters: Optional[Dict[str, Union[str, List[str]]]] = None,
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    """
    On-the-fly text→vector search (knn_text_to_vector) via `/select`.
    """
    params: Dict[str, Any] = {
        "q": "*:*",
        "start": (page - 1) * page_size,
        "rows": page_size,
        "wt": "json",
        "knn.fl": "fulltext",
        "knn.q": query,
        "knn.k": top_k,
    }
    for fq in _build_fq(filters):
        params.setdefault("fq", []).append(fq)

    resp = requests.get(f"{SOLR_BASE}/select", params=params)
    resp.raise_for_status()
    resp_json = resp.json()
    data = resp_json.get("response", {})

    items = []
    for doc in data.get("docs", []):
        title = _flatten_string_field(doc.get("title"))
        date = _flatten_string_field(doc.get("date"))
        items.append({
            "id": doc.get("id"),
            "title": title,
            "authors": doc.get("authors", []),
            "date": date,
        })

    return {"items": items, "total": data.get("numFound", 0), "page_size": page_size, "facets": {}}


def vector_search_resources(
    vector: List[float],
    top_k: int = 10,
    filters: Optional[Dict[str, Union[str, List[str]]]] = None,
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    """
    Precomputed-vector search via a POST to Solr’s /select using the JSON-request 'knn' block.
    """
    url = f"{SOLR_BASE}/select?wt=json"

    # Build the JSON body
    body: Dict[str, Any] = {
        "query": "*:*",
        "start": (page - 1) * page_size,
        "rows": page_size,
        "knn": {
            "field":  "emb_vector",
            "k":      top_k,
            "vector": vector
        }
    }

    # If you have filter queries, add them under "filter" (array of strings)
    if filters:
        body["filter"] = _build_fq(filters)  # e.g. ["provider:peer-reviewed", ...]

    resp = requests.post(
        url,
        json=body,
        headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json().get("response", {})

    items = []
    for doc in data.get("docs", []):
        title = _flatten_string_field(doc.get("title"))
        date = _flatten_string_field(doc.get("date"))
        items.append({
            "id":  doc.get("id"),
            "title": title,
            "authors": doc.get("authors", []),
            "date": date,
        })

    return {
        "items": items,
        "total": data.get("numFound", 0),
        "page_size": page_size,
        "facets": {},
    }
