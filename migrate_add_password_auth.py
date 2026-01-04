"""
Database migration: Add password authentication fields
Adds password_hash and email_verified to accounts table
Creates refresh_tokens table
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("beaver.db")


def migrate():
    """Run migration to add password auth fields"""
    if not DB_PATH.exists():
        print("❌ Database not found. Please run init_db.py first.")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Check if migration already applied
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "password_hash" in columns:
            print("✅ Migration already applied (password_hash exists)")
        else:
            print("🔄 Adding password_hash column to accounts table...")
            cursor.execute("ALTER TABLE accounts ADD COLUMN password_hash TEXT")
            print("✅ Added password_hash column")
        
        if "email_verified" in columns:
            print("✅ Migration already applied (email_verified exists)")
        else:
            print("🔄 Adding email_verified column to accounts table...")
            cursor.execute("ALTER TABLE accounts ADD COLUMN email_verified BOOLEAN DEFAULT 0 NOT NULL")
            print("✅ Added email_verified column")
        
        # Check if refresh_tokens table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='refresh_tokens'
        """)
        
        if cursor.fetchone():
            print("✅ refresh_tokens table already exists")
        else:
            print("🔄 Creating refresh_tokens table...")
            cursor.execute("""
                CREATE TABLE refresh_tokens (
                    id VARCHAR NOT NULL PRIMARY KEY,
                    token VARCHAR NOT NULL UNIQUE,
                    account_id VARCHAR NOT NULL,
                    is_revoked BOOLEAN NOT NULL DEFAULT 0,
                    expires_at DATETIME NOT NULL,
                    created_at DATETIME,
                    FOREIGN KEY(account_id) REFERENCES accounts(id)
                )
            """)
            cursor.execute("CREATE INDEX ix_refresh_tokens_token ON refresh_tokens(token)")
            cursor.execute("CREATE INDEX ix_refresh_tokens_account_id ON refresh_tokens(account_id)")
            print("✅ Created refresh_tokens table")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Running database migration: Add Password Authentication")
    print("=" * 60)
    migrate()
    print("=" * 60)

