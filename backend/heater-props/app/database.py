# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import get_settings

settings = get_settings()

# Create SQLite engine with better concurrency handling
engine = create_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False,  # Needed for SQLite
        "timeout": 30  # Wait up to 30 seconds if database is locked
    },
    poolclass=StaticPool,  # Use single connection pool for SQLite
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()