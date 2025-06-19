
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# point this at your Postgres container (or override via env var)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/digital_ecology"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Each request gets its own Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# Base class for all ORM models
Base = declarative_base()