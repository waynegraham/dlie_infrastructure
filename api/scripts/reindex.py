from database import SessionLocal
from solr_client import reindex_all

if __name__ == "__main__":
    db = SessionLocal()
    print("Reindexing all resources…")
    reindex_all(db)
    print("Done.")