import pysolr
from config import SOLR_URL

_solr = pysolr.Solr(SOLR_URL, always_commit=True)

def index_resource(doc: dict):
    """Index a single resource doc in Solr."""
    _solr.add([doc])

def delete_resource(resource_id: int):
    """Remove a resource from the Solr index."""
    _solr.delete(id=str(resource_id))

def reindex_all(db_session):
    """Fetch all resources from the DB and bulk‐index them."""
    from models import ResourceModel
    docs = []
    for r in db_session.query(ResourceModel).all():
        docs.append({
            "id": str(r.id),
            "title": r.title,
            "abstract": r.abstract,
            "authors": r.authors,
            "date": r.date.isoformat(),
            "provider": r.provider,
            "keywords": r.keywords,
            "fulltext": r.fulltext or "",
            "url": r.url or "",
            # …any other fields you want to make searchable…
        })
    _solr.add(docs)