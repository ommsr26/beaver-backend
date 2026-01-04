"""
Database initialization script for Beaver API Gateway
Run this script to create all database tables
"""
from app.database.db import engine, Base
from app.database.models import Account, APIKey, UsageLog, Transaction, Model, RefreshToken

def init_db():
    """Create all database tables"""
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("\nTables created:")
    print("  - accounts")
    print("  - api_keys")
    print("  - usage_logs")
    print("  - transactions")
    print("  - models")
    print("  - refresh_tokens")

if __name__ == "__main__":
    init_db()

