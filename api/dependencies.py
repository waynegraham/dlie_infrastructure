"""
Shared dependencies for the API routers.
"""
from api.database import SessionLocal


def get_db():
    """Yields a database session and ensures it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
