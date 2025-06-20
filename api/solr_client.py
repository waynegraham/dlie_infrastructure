# api/solr_client.py

import pysolr
from api.config import settings

_solr = pysolr.Solr(str(settings.solr_url), always_commit=True, timeout=10)

def index_resource(doc: dict):
    _solr.add([doc])

def delete_resource(resource_id: int):
    _solr.delete(id=str(resource_id))

def search_resources(
    q: str,
    page: int = 1,
    page_size: int = 10,
    facet_fields: list[str] = None,
    facet_limit: int = 10,
):
    params = {
        "start": (page - 1) * page_size,
        "rows": page_size,
    }
    if facet_fields:
        params.update({
            "facet": "true",
            "facet.field": facet_fields,
            "facet.limit": facet_limit,
        })

    results = _solr.search(q or "*:*", **params)

    items = []
    for doc in results.docs:
        # title and date may come back as single-element lists
        raw_title = doc.get("title")
        title = raw_title[0] if isinstance(raw_title, list) else raw_title

        raw_date = doc.get("date")
        date = raw_date[0] if isinstance(raw_date, list) else raw_date

        items.append({
            "id": doc.get("id"),
            "title": title,
            "authors": doc.get("authors", []),
            "date": date,
        })

    # parse facets
    facets = {}
    if facet_fields:
        facet_counts = results.facets.get("facet_fields", {})
        for field in facet_fields:
            counts = facet_counts.get(field, [])
            facets[field] = [
                {"label": counts[i], "value": counts[i], "count": counts[i+1]}
                for i in range(0, len(counts), 2)
            ]

    return {
        "items": items,
        "total": results.hits,
        "page_size": page_size,
        "facets": facets,
    }