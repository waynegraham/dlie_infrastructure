#!/usr/bin/env python3
# api/scripts/reindex.py

import math
from sqlalchemy import create_engine, MetaData, select, func
from api.config import settings
from api.solr_client import index_resources

# 1) Set up the DB engine and reflect only the 'resources' table
engine = create_engine(settings.database_url)
metadata = MetaData()
metadata.reflect(bind=engine, only=['resources'])
resources_tbl = metadata.tables['resources']

# 2) Calculate total rows and batch info
BATCH_SIZE = 200
with engine.connect() as conn:
    total = conn.execute(select(func.count()).select_from(resources_tbl)).scalar_one()
batches = math.ceil(total / BATCH_SIZE)
print(f"Reindexing {total} resources in {batches} batches…")

# 3) Iterate through batches and index
with engine.connect() as conn:
    for batch_num in range(batches):
        offset = batch_num * BATCH_SIZE
        stmt = select(resources_tbl).offset(offset).limit(BATCH_SIZE)
        result = conn.execute(stmt)
        rows = result.mappings().all()

        docs = []
        for row in rows:
            doc = {
                "id":            str(row["id"]),
                "title":         row.get("title", ""),
            # Map the DB column 'type' to Solr field 'resource_type'
            "resource_type": row.get("type", ""),
                "date":          row.get("date").isoformat() + "Z" if row.get("date") else "",
                "authors":       row.get("authors") or [],
                "abstract":      row.get("abstract") or "",
                "doi":           row.get("doi") or "",
                "url":           row.get("url") or "",
                "keywords":      row.get("keywords") or [],
                "provider":      row.get("provider") or "",
                "fulltext":      row.get("fulltext") or "",
            }
            docs.append(doc)

        print(f"  🗂  Batch {batch_num+1}/{batches}: indexing {len(docs)} docs...")
        index_resources(docs)
        print("    ✅ Done.")

print("🎉 Reindex complete!")
