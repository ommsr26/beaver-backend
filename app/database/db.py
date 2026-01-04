"""
Centralized database configuration
Supports both SQLite (dev) and PostgreSQL (prod)
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool, QueuePool
from sqlalchemy.engine import Engine
from typing import Optional

from app.config import settings

# Determine database URL
if settings.DATABASE_URL:
    DATABASE_URL = settings.DATABASE_URL
else:
    # Default to SQLite for development
    DATABASE_URL = "sqlite:///./beaver.db"

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for SQL query logging
    )
    
    # Enable foreign key constraints for SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before using
        echo=False  # Set to True for SQL query logging
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_database_url() -> str:
    """Get the current database URL"""
    return DATABASE_URL


def is_postgresql() -> bool:
    """Check if using PostgreSQL"""
    return DATABASE_URL.startswith("postgresql")


def is_sqlite() -> bool:
    """Check if using SQLite"""
    return DATABASE_URL.startswith("sqlite")
